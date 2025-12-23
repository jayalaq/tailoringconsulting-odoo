from odoo import fields, models, api, _

class PleInvBalLines09(models.Model):
    _name = 'ple.report.inv.bal.line.09'
    _description = 'Cuentas por cobrar - Líneas'

    ple_report_inv_val_09_id = fields.Many2one(
        comodel_name='ple.report.inv.bal.09',
        string='Reporte de Estado de Situación financiera'
    )
    name = fields.Char()
    ple_correlative = fields.Char()
    ple_selection = fields.Char()
    code_prefix_start = fields.Char()
    initial_balance_amortization = fields.Integer()
    name_aml = fields.Char()
    code_account = fields.Char()
    date = fields.Char()
    balance = fields.Float()
    balance_amortization = fields.Float()
    balance_amortization_xls = fields.Float()
    operation_date = fields.Date()
    state = fields.Char()
    name_s = fields.Char()