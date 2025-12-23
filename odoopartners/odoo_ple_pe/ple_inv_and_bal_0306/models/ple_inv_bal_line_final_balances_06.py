from odoo import fields, models

class PleInvBalLineFinalBalances06(models.Model):
    _name = 'ple.inv.bal.line.final.balances.06'
    _description = 'Ple Inv Bal Line Final Balances 06'
    _order = 'name desc'

    name = fields.Char(string='Periodo')
    document_name = fields.Char(string='CUO')
    correlative = fields.Char(string='Correlativo')
    type_document_debtor = fields.Char(string='Tipo de documento del deudor')
    tax_identification_number = fields.Char(string='Número de documento deudor')
    business_name = fields.Char(string='Razon social del deudor')
    type_document = fields.Char(string='Tipo de CPE de la cuenta por cobrar')
    number_serie = fields.Char(string='Número de serie del comprobante de pago')
    number_document = fields.Char(string='Número del comprobante de pago')
    date_of_issue = fields.Char(string='Fecha de emisión del comprobante de pago')
    provisioned_invoice = fields.Char(string='Factura provisionada')
    provision_amount = fields.Float(string='Monto de la provisión')
    state = fields.Char(string='Indica el estado de la operación')
    ple_report_inv_val_06_id = fields.Many2one(comodel_name='ple.report.inv.bal.06', string='Reporte PLE 0306')