from odoo import fields, models


class PleInvBalLines(models.Model):
    _name = 'ple.report.inv.bal.line.15'
    _description = 'Reporte 3.15 - Líneas'

    catalog_code = fields.Char(string='Código de catálogo')
    document_name = fields.Char(string='Nombre del documento')
    name = fields.Char(string='Periodo')
    accounting_seat = fields.Char(string='CUO')
    serial_number_payment = fields.Char(string='Número Serie del Comprobante de Pago')
    related_payment_voucher = fields.Char(string='Número del Comprobante de Pago Relacionado')
    correlative = fields.Char(string='Correlativo')
    ref = fields.Char(string='Referencia Factura')
    type_l10n_latam_identification = fields.Char(string='Tipo de Comprobante de Pago')
    code = fields.Char(string='Código de la Cuenta Contable')
    additions = fields.Float(string='Adiciones')
    deductions = fields.Float(string='Deducciones')
    outstanding_balance = fields.Float(string='Saldo Pendiente')
    free_field = fields.Char(string='Campo libre')
    ple_report_inv_val_15_id = fields.Many2one(comodel_name='ple.report.inv.bal.one')