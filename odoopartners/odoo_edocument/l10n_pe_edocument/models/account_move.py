from odoo import api, fields, models
from odoo.exceptions import UserError
from odoo.tools.float_utils import float_repr, float_round


refund_reason_13 = ('13', 'Corrección del monto neto pendiente de pago y/o la(s) de vencimiento del \n pago único o de las cuotas y/o los montos '
                          'correspondientes a cada cuota , de ser el caso')


class AccountMove(models.Model):
    _inherit = 'account.move'

    agent_retention = fields.Boolean(string='Retención?')
    base_amount_retention = fields.Float(string='Base imponible de la retención')
    multiplier_factor_field = fields.Char(
        string='Multiplier Label', 
        compute='_compute_multiplier_factor_field', 
        store=True
    )
    amount_field_advance = fields.Char(
        string='Amount Label', 
        compute='_compute_multiplier_factor_field', 
        store=True
    )
    debit_field_advance = fields.Char(
        string='Debit Label', 
        compute='_compute_multiplier_factor_field', 
        store=True
    )
    porcentage_retention = fields.Char(
        string='Porcentaje de retención',
        compute='_compute_porcentage_retention',
        readonly=True
    )
    amount_retention_IGV = fields.Float(
        string='Monto de la retención',
        compute='_compute_amount_retention_IGV'
    )
    payment_method_id = fields.Many2one(
        comodel_name='payment.methods.codes',
        string='Medio de pago',
    )
    l10n_pe_edi_refund_reason = fields.Selection(selection_add=[refund_reason_13])
    related_tax_documents_code = fields.Selection(
        selection=[
            ('01', 'Factura - emitida para corregir error en el RUC'),
            ('02', 'Factura - emitida por anticipos'),
            ('03', 'Boleta de venta - Emitida por anticipos'),
            ('04', 'Ticket de salida - ENAPU'),
            ('05', 'Código SCOP'),
            ('06', 'Factura electrónica remitente'),
            ('07', 'Guía de remisión remitente'),
            ('08', 'Declaración de salida del depósito franco'),
            ('09', 'Declaración simplificada de importación'),
            ('10', 'Liquidación de compra - emitida por anticipos'),
            ('99', 'Otros'),
        ], 
        string='Código de documentos relacionados tributarios'
    )

    @api.onchange('l10n_pe_edi_operation_type')
    def _onchange_payment_method(self):
        transfer_funds = self.env['payment.methods.codes'].search(
            [('code', '=', '003')], 
            limit=1
        )
        if self.l10n_pe_edi_operation_type in ['1001', '1002', '1003', '1004'] and any(transfer_funds):
            self.payment_method_id = transfer_funds.id
        else:
            self.payment_method_id = None

    @api.depends('invoice_payment_term_id', 'agent_retention', 'invoice_line_ids')
    def _compute_multiplier_factor_field(self):
        # TODO: Refactor very simple logic :/
        for move in self:
            if move.invoice_payment_term_id and move.invoice_payment_term_id.line_ids:
                for payment in move.invoice_payment_term_id.line_ids:
                    if payment.l10n_pe_is_detraction_retention:
                        move.multiplier_factor_field = str(round(payment.value_amount / 100, 4))
                        break
            else:
                move.multiplier_factor_field = False

            if move.line_ids:
                for line in move.line_ids:
                    if line.l10n_pe_is_detraction_retention:
                        move.amount_field_advance = str(round(line.amount_currency, 2))
                        move.debit_field_advance = str(round(abs(move.amount_total), 2))
                        break
            else:
                move.amount_field_advance = False
                move.debit_field_advance = False

    @api.depends('porcentage_retention')
    def _compute_porcentage_retention(self):
        for move in self:
            move.porcentage_retention = '3%'

    @api.depends('amount_retention_IGV')
    def _compute_amount_retention_IGV(self):
        for move in self:
            move.amount_retention_IGV = move.base_amount_retention * 0.03
            move.amount_retention_IGV = '{0:.2f}'.format(move.amount_retention_IGV)

    def action_post(self):
        peru_id = self.env.ref('base.pe')
        for move in self:
            max_percent = any(move.invoice_line_ids.mapped('product_id.l10n_pe_withhold_code'))
            is_detraction = any(
                move.invoice_payment_term_id.line_ids.mapped(
                    'l10n_pe_is_detraction_retention'
                )
            )
            payment_means_codes = ['1001', '1002', '1003', '1004']
            detraction_operation_type = move.l10n_pe_edi_operation_type in payment_means_codes
            exportation_codes = ['0201', '0202', '0203', '0204', '0205', '0206', '0207', '0208']
            detraction_operation_type |= move.l10n_pe_edi_operation_type in exportation_codes
            if (
                move.l10n_latam_document_type_id
                and move.l10n_latam_document_type_id.code == '01'
                and peru_id == move.env.company.country_id
                and (max_percent or is_detraction)
                and (move.amount_total_signed >= 700 and not detraction_operation_type)
                and (
                    not move.agent_retention
                    and move.journal_id.type == 'sale'
                    and move.journal_id.l10n_latam_use_documents
                )
            ):
                raise UserError(
                    "Operación sujeta a detracción que supera la cantidad, debe indicar en el campo "
                    '"operation type" que es afecta a detracción, por lo que la factura no puede '
                    "ser publicada hasta que arregle el error."
                )
        return super(AccountMove, self).action_post()

    def _l10n_pe_edi_get_spot(self):
        spot = super(AccountMove, self)._l10n_pe_edi_get_spot()
        max_percent = max(self.invoice_line_ids.mapped('product_id.l10n_pe_withhold_percentage'), default=0)
        spot.update({'payment_means_code': self.payment_method_id.code}) if spot else spot
        return spot
