from odoo import fields, models, api

class PleAdditionDeduction(models.Model):
    _name = 'ple.addition.deduction'
    _description = 'ple addition deduction'

    ple_report_inv_val_seventeen_id = fields.Many2one(
        comodel_name='ple.report.inv.bal.seventeen',
        string='Reporte de Estado de Situación financiera'
    )
    transfers_additions_selection = fields.Selection(
        selection=[
            ('additions', 'Adiciones'),
            ('deductions', 'Deducciones'),
        ],
        string='Adiciones y deducciones'
    )
    trial_balances_catalog_id = fields.Many2one(
        string='Cuenta de balance de comprobación',
        comodel_name='trial.balances.catalog'
    )
    amount = fields.Char(
        string='Importe'
    )