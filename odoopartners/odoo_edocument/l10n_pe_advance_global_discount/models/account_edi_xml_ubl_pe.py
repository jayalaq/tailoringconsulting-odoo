from odoo import models
from odoo.exceptions import UserError


class AccountEdiXmlUBLPE(models.AbstractModel):
    _inherit = 'account.edi.xml.ubl_pe'

    def _export_invoice_vals(self, invoice):
        vals = super()._export_invoice_vals(invoice)
        special_invoice_lines = invoice.invoice_line_ids.filtered(
            lambda l: l.display_type not in ('line_note', 'line_section')
                      and l.price_subtotal < 0
                      and (l.product_id.l10n_pe_advance or l.product_id.global_discount)
        )
        if special_invoice_lines:
            vals.update({
                'InvoiceType_template': 'l10n_pe_advance_global_discount.ubl_21_InvoiceType_edocument',
            })
            self._l10n_pe_edi_set_advance_global_discount_values(vals, invoice, special_invoice_lines)
        return vals

    @staticmethod
    def _l10n_pe_edi_set_advance_global_discount_values(values, move_id, special_lines):
        """
        Filter and separate special lines (Example: Global discount and advance lines)
        """
        advance_lines_vals = []
        discount_lines_vals = []
        i = 1
        total_advance = 0.00
        total_discount = 0.00

        discount_percent_global = move_id.discount_percent_global / 100
        line_extension_amount = 0
        tax_inclusive_amount = 0
        for line in special_lines:
            # Advance line
            if line.product_id.l10n_pe_advance:
                if not line.l10n_pe_advance_invoice:
                    raise UserError(f'{line.product_id.name}: Nombre de Anticipo vácio.')
                if move_id.l10n_latam_document_type_id.code == '01':
                    document_type_id_code = '02'
                elif move_id.l10n_latam_document_type_id.code == '03':
                    document_type_id_code = '03'
                else:
                    document_type_id_code = move_id.l10n_latam_document_type_id.code or ''
                advance_line = {
                    'id': i,
                    'company_vat': move_id.company_id.vat,
                    'currency_name': line.currency_id.name,
                    'advance_name': line.l10n_pe_advance_invoice.replace('\n', '').replace(' ', ''),
                    'document_type_code': document_type_id_code,
                    'partner_document_type_code': '6' if move_id.partner_id.l10n_latam_identification_type_id.l10n_pe_vat_code != '6' else move_id.partner_id.l10n_latam_identification_type_id.l10n_pe_vat_code,
                    'paid_amount': abs(line.price_total),
                    'line': line
                }
                total_advance += advance_line['paid_amount']
                advance_lines_vals.append(advance_line)
                i += 1

            # Discount global line
            if line.product_id.global_discount:
                product_id = line.product_id
                reason_code = product_id.l10n_pe_charge_discount_id and product_id.l10n_pe_charge_discount_id.code or '00'
                discount_global_line = {
                    'line': line,
                    'discount_charge_indicator': 'false' if reason_code not in ['45', '46', '47'] else 'true',
                    'discount_allowance_charge_reason_code': reason_code,
                    'discount_percent': discount_percent_global,
                    'discount_amount': abs(line.price_subtotal),
                    'base_amount': abs(line.price_subtotal / discount_percent_global),
                }
                if reason_code == '03':
                    total_discount += abs(line.price_subtotal)

                discount_lines_vals.append(discount_global_line)

        for positive_line in move_id.invoice_line_ids.filtered(lambda l: not l.product_id.l10n_pe_advance):
            line_extension_amount += positive_line.price_subtotal
            tax_inclusive_amount += positive_line.price_total
        
        # Apply rounding
        base_total = tax_inclusive_amount - total_advance
        rounded_total = move_id.currency_id.round(base_total)

        # Calculate rounding difference
        if move_id.invoice_cash_rounding_id:
            rounding_amount = move_id.invoice_cash_rounding_id.compute_difference(
                move_id.currency_id,
                base_total
            )
        else:
            rounding_amount = rounded_total - base_total

        values['vals']['monetary_total_vals'].update({
            'line_extension_amount': line_extension_amount,
            'tax_inclusive_amount': tax_inclusive_amount + rounding_amount,
            'payable_amount': (tax_inclusive_amount - total_advance) + rounding_amount,
            'prepaid_amount': total_advance,
            'allowance_total_amount': total_discount,
        })
        if advance_lines_vals:
            values['vals'].update({
                'advance_invoice_vals': advance_lines_vals,
                'total_advance': total_advance,
                'advance_invoice': True
            })

        if discount_lines_vals:
            values['vals'].update({
                'discount_lines_vals': discount_lines_vals,
                'total_discount': total_discount,
                'discount_invoice': True
            })

    def _get_filter_taxable_amount_tax_amount(self, line):
        return line.display_type not in ('line_note', 'line_section') and line.price_total < 0 and (
                line.product_id.l10n_pe_advance or line.product_id.global_discount)
