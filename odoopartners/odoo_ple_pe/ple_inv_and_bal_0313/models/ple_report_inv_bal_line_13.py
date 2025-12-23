from odoo import fields, models, api

class PleInvBalLines(models.Model):
    _name = 'ple.report.inv.bal.line.13'
    _description = 'Reporte 3.13 - Líneas'

    catalog_code = fields.Char(string='Código de catálogo')
    document_name = fields.Char(string='Nombre de la Factura')
    name = fields.Char(string="Periodo")
    accounting_seat = fields.Char(string="CUO")
    correlative = fields.Char(string="Correlativo")
    type_document_third = fields.Integer(string="Tipo de Documento Tercero")
    tax_identification_number = fields.Char(
        string="Numero de Documento Tercero")
    date_issue = fields.Date(string='Fecha de Emisión del Comprobante de Pago')
    code = fields.Char(string='Código de la Cuenta Contable')
    business_name = fields.Char(string="Apellidos y Nombres de Terceros")
    provision_amount = fields.Float(
        string="Monto Pendiente de Pago al Tercero")
    account_status = fields.Integer(string="Estado de la operación")
    free_field = fields.Char(string="Campo libre")
    ple_report_inv_val_13_id = fields.Many2one(
        comodel_name='ple.report.inv.bal.one')