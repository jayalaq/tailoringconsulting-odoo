from odoo import models
from odoo.exceptions import UserError
from odoo.addons.l10n_pe_edi.models.account_edi_xml_ubl_pe import FREE_AFFECTATION_REASONS


class AccountEdiXmlUBLPE(models.AbstractModel):
    _inherit = 'account.edi.xml.ubl_pe'

    def _l10n_pe_edi_get_order_reference(self, invoice):
        move_ref = invoice.ref
        sales_order_name = 'sale_line_ids' in invoice.invoice_line_ids._fields and ','.join(
            invoice.invoice_line_ids.sale_line_ids.order_id.mapped('name')
        )
        move_name = invoice.name

        order_reference = ''
        if move_ref:
            order_reference = str(move_ref).strip()
        elif sales_order_name:
            order_reference = str(sales_order_name).strip()
        elif move_name:
            order_reference = str(move_name).strip()

        if order_reference or order_reference != '':
            special_character = "¿?|°<>[]/'@!¡#$%^&*()´+\t.,:;\n"
            for x in range(len(special_character)):
                order_reference = order_reference.replace(
                    special_character[x], '')
            order_reference = order_reference.replace(special_character, '')
            order_reference = order_reference.replace(' ', '')
        return order_reference[:20]

    def _export_invoice_vals(self, invoice):
        vals = super()._export_invoice_vals(invoice)

        vals.update({
            'InvoiceType_template': 'l10n_pe_edocument.ubl_21_InvoiceType_edocument',
        })

        vals['vals'].update({
            'order_reference': self._l10n_pe_edi_get_order_reference(invoice),
            'currency': invoice.currency_id,
        })

        # Credit Note specific changes
        if vals['document_type'] == 'credit_note':
            if invoice.l10n_latam_document_type_id.code == '07':
                if 'discrepancy_response_vals' in vals['vals']:
                    vals['vals']['discrepancy_response_vals'][0]['description'] = invoice.l10n_pe_edi_cancel_reason
            if invoice.origin_number and invoice.origin_l10n_latam_document_type_id:
                vals['vals'].update({
                    'billing_reference_vals': {
                        'id': invoice.origin_number.replace(' ', ''),
                        'document_type_code': invoice.origin_l10n_latam_document_type_id.code,
                    },
                })

        # Debit Note specific changes
        if vals['document_type'] == 'debit_note':
            if invoice.l10n_latam_document_type_id.code == '08':
                if 'discrepancy_response_vals' in vals['vals']:
                    vals['vals']['discrepancy_response_vals'][0]['description'] = invoice.l10n_pe_edi_cancel_reason
            if invoice.origin_number and invoice.origin_l10n_latam_document_type_id:
                vals['vals'].update({
                    'billing_reference_vals': {
                        'id': invoice.origin_number.replace(' ', ''),
                        'document_type_code': invoice.origin_l10n_latam_document_type_id.code,
                    },
                })

        if invoice.carrier_ref_number:
            vals['vals'].update({
                'despatch_document_reference': str(invoice.carrier_ref_number).replace('\n', '').replace(' ', '')[:30],
                'despatch_document_reference_type_code': '09',
            })

        if invoice.aditional_document_reference:
            vals['vals'].update({
                'additional_document_reference': str(invoice.aditional_document_reference).replace('\n', '').replace(' ', '')[:30],
                'additional_document_reference_type_code': invoice.related_tax_documents_code or '',
            })

        # Retention
        if invoice.agent_retention:
            vals['vals'].update({
                'retention_invoice': True,
                'retention_invoice_charge_indicator': 'false',
                'retention_invoice_allowance_charge_reason_code': '62',
                'retention_invoice_multiplier_factor_numeric': invoice.multiplier_factor_field,
                'retention_invoice_amount': invoice.amount_field_advance,
                'retention_invoice_base_amount': invoice.debit_field_advance,
            })

        # Consider lines whose line_price_subtotal is greater than 0
        vals['vals']['line_vals'] = [
            line
            for line in vals['vals']['line_vals']
            if float(line['line_price_subtotal']) > 0
        ]

        return vals

    def _get_partner_party_legal_entity_vals_list(self, partner):
        vals = super()._get_partner_party_legal_entity_vals_list(partner)
        for val in vals:
            registration_name = partner.name
            if partner and partner.name and partner.parent_id and partner.parent_id.name:
                registration_name += ', ' + partner.parent_id.name
            val.update({'registration_name': registration_name})
        return vals

    def _get_partner_address_vals(self, partner):
        vals = super()._get_partner_address_vals(partner)

        def replace_empty_values(d):
            for k, v in d.items():
                if isinstance(v, dict):
                    d[k] = replace_empty_values(v)
                elif not v:
                    d[k] = '-'
            return d

        vals = replace_empty_values(vals)
        return vals

    def _get_invoice_payment_terms_vals_list(self, invoice):
        # OVERRIDE l10n_pe_edi -> Change spot calc and impact over payment terms vals
        spot = invoice._l10n_pe_edi_get_spot()
        invoice_date_due_vals_list = []
        for rec_line in invoice.line_ids.filtered(lambda l: l.account_type == 'asset_receivable' and not l.l10n_pe_is_detraction_retention):
            invoice_date_due_vals_list.append({
                'currency_name': rec_line.currency_id.name,
                'currency_dp': rec_line.currency_id.decimal_places,
                'amount': abs(rec_line.amount_currency),
                'date_maturity': rec_line.date_maturity,
            })
        total_after_spot = sum(due_vals['amount'] for due_vals in invoice_date_due_vals_list)
        payment_means_id = invoice._l10n_pe_edi_get_payment_means()
        vals = []
        if spot:
            vals.append({
                'id': spot['id'],
                'currency_name': 'PEN',
                'currency_dp': 2,
                'payment_means_id': spot['payment_means_id'],
                'payment_percent': spot['payment_percent'],
                'amount': spot['amount'],
            })
        if (invoice.l10n_pe_edi_refund_reason == '13' and invoice.move_type == 'out_refund') or invoice.move_type not in ('out_refund', 'in_refund'):
            if payment_means_id == 'Contado':
                vals.append({
                    'id': 'FormaPago',
                    'payment_means_id': payment_means_id,
                })
            else:
                vals.append({
                    'id': 'FormaPago',
                    'currency_name': invoice.currency_id.name,
                    'currency_dp': invoice.currency_id.decimal_places,
                    'payment_means_id': payment_means_id,
                    'amount': total_after_spot,
                })
                for i, due_vals in enumerate(invoice_date_due_vals_list):
                    vals.append({
                        'id': 'FormaPago',
                        'currency_name': due_vals['currency_name'],
                        'currency_dp': due_vals['currency_dp'],
                        'payment_means_id': 'Cuota' + '{0:03d}'.format(i + 1),
                        'amount': abs(due_vals['amount']) if invoice.l10n_pe_edi_refund_reason == '13' else due_vals['amount'],
                        'payment_due_date': due_vals['date_maturity'],
                    })
        return vals

    def _get_invoice_tax_totals_vals_list(self, invoice, taxes_vals):
        tax_subtotal_vals = super()._get_invoice_tax_totals_vals_list(invoice, taxes_vals)

        invoice_lines = invoice.invoice_line_ids.filtered(
            lambda line: line.display_type not in ('line_note', 'line_section') and
                         (self._check_line_withdrawal_tax(line) or self._check_line_unaffected_tax(line))
        )
        if invoice_lines:
            sum_taxable_amount = 0
            sum_tax_amount = 0
            tax_code_11 = 0
            for line in invoice_lines:
                taxable_amount, tax_amount = self._get_line_taxable_amount_tax_amount(line)
                is_line_withdrawal_tax = self._check_line_withdrawal_tax(line)
                is_line_unaffected_tax = self._check_line_unaffected_tax(line)

                if is_line_withdrawal_tax or is_line_unaffected_tax:
                    if line.l10n_pe_edi_affectation_reason == '11':
                        tax_code_11 += (tax_amount * -1)
                    sum_tax_amount += tax_amount
                    sum_taxable_amount += taxable_amount

            for tax in [
                tax_val
                for tax_val in tax_subtotal_vals[0]['tax_subtotal_vals']
                if tax_val['tax_category_vals']['tax_scheme_vals']['name'] == 'GRA'
            ]:
                tax['taxable_amount'] = sum_taxable_amount
                tax['tax_amount'] = abs(tax_code_11)

            total_tax_amount = sum(tax['tax_amount'] for tax in tax_subtotal_vals[0]['tax_subtotal_vals'])
            tax_subtotal_vals[0]['tax_amount'] = total_tax_amount - sum_tax_amount

        # Special case l10n_pe_edi_refund_reason = 13
        if invoice.l10n_pe_edi_refund_reason == '13':
            for tax in [
                tax_val
                for tax_val in tax_subtotal_vals[0]['tax_subtotal_vals']
            ]:
                tax_subtotal_vals[0]['tax_amount'] = 0
                tax['taxable_amount'] = 0
                tax['tax_amount'] = 0

        # Add ICBPER tax amount to the total tax amount
        for tax in tax_subtotal_vals[0]['tax_subtotal_vals']:
            if tax['tax_category_vals']['tax_scheme_vals']['id'] == '7152':
                tax_subtotal_vals[0]['tax_amount'] += tax['tax_amount']
        return tax_subtotal_vals

    def _get_invoice_line_item_vals(self, line, taxes_vals):
        vals = super()._get_invoice_line_item_vals(line, taxes_vals)

        is_line_withdrawal_tax = self._check_line_withdrawal_tax(line)
        is_line_unaffected_tax = self._check_line_unaffected_tax(line)

        if is_line_withdrawal_tax or is_line_unaffected_tax:
            tax_id = line.tax_ids[0]
            vals.update({
                'classified_tax_category_vals': [{
                    'id': tax_id.l10n_pe_edi_unece_category,
                    'tax_scheme_vals': {'id': tax_id.tax_group_id.name}
                }],
                'tax_category_code': tax_id.l10n_pe_edi_unece_category
            })

        return vals

    def _get_invoice_line_price_vals(self, line):
        vals = super()._get_invoice_line_price_vals(line)

        price_precision = self.env['decimal.precision'].precision_get('Product Price')
        is_line_withdrawal_tax = self._check_line_withdrawal_tax(line)
        is_line_unaffected_tax = self._check_line_unaffected_tax(line)

        if is_line_withdrawal_tax or is_line_unaffected_tax or line.move_id.l10n_pe_edi_refund_reason == '13':  # Special case l10n_pe_edi_refund_reason = 13
            vals.update({'price_amount': float(self.format_float(0, price_precision))})

        return vals

    def _get_invoice_line_vals(self, line, line_id, taxes_vals):
        vals = super()._get_invoice_line_vals(line, line_id, taxes_vals)
        is_line_withdrawal_tax = self._check_line_withdrawal_tax(line)
        is_line_unaffected_tax = self._check_line_unaffected_tax(line)
        if is_line_withdrawal_tax or is_line_unaffected_tax:
            taxable_amount, tax_amount = self._get_line_taxable_amount_tax_amount(line)
            vals['pricing_reference_vals']['alternative_condition_price_vals'][0]['price_amount'] = taxable_amount / line.quantity
            vals['line_extension_amount'] = taxable_amount

        # Special case l10n_pe_edi_refund_reason = 13
        if line.move_id.l10n_pe_edi_refund_reason == '13':
            vals['pricing_reference_vals']['alternative_condition_price_vals'][0]['price_amount'] = 0
            vals['line_extension_amount'] = 0

        # Add line_price_subtotal
        vals['line_price_subtotal'] = line.price_subtotal
        if line.l10n_pe_edi_affectation_reason == '21':
            vals['allowance_charge_vals'] = []

        # Remove ICBPER tax from the line_extension_amount line
        for tax_line in vals['tax_total_vals'][0]['tax_subtotal_vals']:
            if tax_line['tax_category_vals']['tax_scheme_vals']['id'] == '7152':
                vals['line_extension_amount'] -= tax_line['tax_amount'] if vals['line_extension_amount'] > tax_line['tax_amount'] else 0.0
                vals['allowance_charge_vals'] = []
        return vals

    def _get_invoice_line_tax_totals_vals_list(self, line, taxes_vals):
        # OVERRIDE l10n_pe_edi
        vals = {
            'currency': line.currency_id,
            'currency_dp': line.currency_id.decimal_places,
            'tax_amount': 0.00 if line.l10n_pe_edi_affectation_reason in FREE_AFFECTATION_REASONS else line.price_total - line.price_subtotal,
            'tax_subtotal_vals': [],
        }

        for tax_detail_vals in taxes_vals['tax_details'].values():
            tax = self.env['account.tax'].browse(tax_detail_vals['group_tax_details'][0]['id'])
            if tax_detail_vals['tax_amount_currency'] < 0 and line.move_id.l10n_pe_edi_legend == '1002':
                continue
            vals['tax_subtotal_vals'].append({
                'currency': line.currency_id,
                'currency_dp': line.currency_id.decimal_places,
                'taxable_amount': tax_detail_vals['base_amount_currency'] if tax.tax_group_id.l10n_pe_edi_code != 'ICBPER' else None,
                'tax_amount': tax_detail_vals['tax_amount_currency'] or 0.0,
                'base_unit_measure_attrs': {
                    'unitCode': line.product_uom_id.l10n_pe_edi_measure_unit_code,
                },
                'base_unit_measure': int(line.quantity) if tax.tax_group_id.l10n_pe_edi_code == 'ICBPER' else None,
                'tax_category_vals': {
                    'percent': tax.amount if tax.amount_type == 'percent' else None,
                    # Modify the tax_exemption_reason_code validation over ICBPER tax and
                    # validate directly over the tax and not the line because line always work with the first tax
                    'tax_exemption_reason_code': (
                        tax.l10n_pe_edi_affectation_reason
                        if tax.tax_group_id.l10n_pe_edi_code not in ['ICBPER'] and tax.l10n_pe_edi_affectation_reason else None
                    ),
                    'tier_range': tax.l10n_pe_edi_isc_type if tax.tax_group_id.l10n_pe_edi_code == 'ISC' and tax.l10n_pe_edi_isc_type else None,
                    'tax_scheme_vals': {
                        'id': tax.l10n_pe_edi_tax_code,
                        'name': tax.tax_group_id.l10n_pe_edi_code,
                        'tax_type_code': tax.l10n_pe_edi_international_code,
                    },
                },
            })

        # Own code
        is_line_withdrawal_tax = self._check_line_withdrawal_tax(line)
        is_line_unaffected_tax = self._check_line_unaffected_tax(line)

        tax_vals = vals
        tax_subtotal_vals = tax_vals.get('tax_subtotal_vals', [{}])

        if not tax_subtotal_vals:
            tax_vals['tax_subtotal_vals'] = [{}]
            return [tax_vals]

        if is_line_withdrawal_tax or is_line_unaffected_tax:
            taxable_amount, tax_amount = self._get_line_taxable_amount_tax_amount(line)

            tax_vals['tax_amount'] = 0  # tax_amount
            tax_subtotal_vals[0]['taxable_amount'] = taxable_amount
            tax_subtotal_vals[0]['tax_amount'] = tax_amount

        # Special case l10n_pe_edi_refund_reason = 13
        if line.move_id.l10n_pe_edi_refund_reason == '13':
            tax_vals['tax_amount'] = 0
            tax_subtotal_vals[0]['taxable_amount'] = 0
            tax_subtotal_vals[0]['tax_amount'] = 0
        if line.l10n_pe_edi_affectation_reason == '21':
            tax_vals['tax_amount'] = 0.0
            tax_subtotal_vals[0]['tax_amount'] = 0.0
        return [tax_vals]

    def _get_line_taxable_amount_tax_amount(self, line):
        # TODO: OVERRIDE
        if line.display_type == 'product' and line.move_id.is_invoice(True):
            amount_currency = line.price_unit * (1 - line.discount / 100)
            handle_price_include = True
            quantity = line.quantity
        else:
            amount_currency = line.amount_currency
            handle_price_include = False
            quantity = 1

        compute_all_currency = line.tax_ids.compute_all(
            amount_currency,
            currency=line.currency_id,
            quantity=quantity,
            product=line.product_id,
            partner=line.move_id.partner_id or line.partner_id,
            is_refund=line.is_refund,
            handle_price_include=handle_price_include,
            include_caba_tags=line.move_id.always_tax_exigible,
        )

        taxable_amount = compute_all_currency['total_excluded']
        tax_amount = sum(
            tax['amount']
            for tax in compute_all_currency['taxes']
            if tax['amount'] > 0
        )

        # TODO: START OVERRIDE
        if self._get_filter_taxable_amount_tax_amount(line):
            total_excluded = compute_all_currency['total_excluded']
            total_included = compute_all_currency['total_included']
            taxable_amount = total_excluded
            tax_amount = total_included - total_excluded
        # TODO: END OVERRIDE

        return taxable_amount, tax_amount

    def _get_filter_taxable_amount_tax_amount(self, line):
        return line.display_type not in ('line_note', 'line_section') and line.price_total < 0

    def _get_invoice_monetary_total_vals(self, invoice, taxes_vals, line_extension_amount, allowance_total_amount, charge_total_amount):
        vals = super()._get_invoice_monetary_total_vals(invoice, taxes_vals, line_extension_amount, allowance_total_amount, charge_total_amount)

        # Initialize amounts
        line_extension_amount = 0
        tax_exclusive_amount = 0
        tax_inclusive_amount = 0
        base_total_sum = 0

        # Filter invoice lines
        invoice_lines = invoice.invoice_line_ids.filtered(lambda line: line.display_type not in ('line_note', 'line_section'))

        for line_id, line in enumerate(invoice_lines):
            is_line_withdrawal_tax = self._check_line_withdrawal_tax(line)
            is_line_unaffected_tax = self._check_line_unaffected_tax(line)

            if is_line_withdrawal_tax or is_line_unaffected_tax:
                continue

            line_taxes_vals = taxes_vals['tax_details_per_record'][line]
            line_vals = self._get_invoice_line_vals(line, line_id, line_taxes_vals)

            taxable_amount, tax_amount = self._get_line_taxable_amount_tax_amount(line)

            # Add to totals if not an excluded tax type
            if not (is_line_withdrawal_tax or is_line_unaffected_tax):
                line_extension_amount += line_vals['line_extension_amount']
                tax_exclusive_amount += taxable_amount
                base_total_sum += taxable_amount + tax_amount
                tax_inclusive_amount += abs(line.price_total)

        base_total = base_total_sum
        rounded_total = invoice.currency_id.round(base_total)
        rounding_diff = rounded_total - base_total

        if invoice.invoice_cash_rounding_id:
            rounding_amount = invoice.invoice_cash_rounding_id.compute_difference(
                invoice.currency_id,
                base_total
            )
        else:
            rounding_amount = rounding_diff
        payable_amount = tax_inclusive_amount

        # Update values
        vals.update({
            'line_extension_amount': line_extension_amount,
            'tax_exclusive_amount': tax_exclusive_amount,
            'tax_inclusive_amount': tax_inclusive_amount + rounding_amount,
            'payable_amount': payable_amount + rounding_amount,
        })

        # Special case l10n_pe_edi_refund_reason = 13
        if invoice.l10n_pe_edi_refund_reason == '13':
            vals.update({
                'line_extension_amount': 0,
                'tax_exclusive_amount': 0,
                'tax_inclusive_amount': 0,
                'allowance_total_amount': 0,
                'payable_amount': 0,
            })
        return vals

    def _check_line_withdrawal_tax(self, line):
        conditions = (
            line.move_id.move_type in ('out_invoice', 'out_refund'),
            line.move_id.country_code == 'PE',
            line.l10n_pe_edi_affectation_reason in ('11', '12', '13', '14', '15', '16')
        )
        return all(conditions)

    def _check_line_unaffected_tax(self, line):
        conditions = (
            line.move_id.move_type in ('out_invoice', 'out_refund'),
            line.move_id.country_code == 'PE',
            line.l10n_pe_edi_affectation_reason in ('21', '31', '32', '33', '34', '35', '36', '37')
        )
        return all(conditions)
