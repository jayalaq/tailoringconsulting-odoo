from odoo import fields, models, api


class PleBalanceInitial(models.Model):
    _name = 'ple.initial.balances.seveenten'
    _order = 'sequence asc'
    _description = 'ple initial balances seveenten'

    ple_report_inv_val_seventeen_id = fields.Many2one(
        comodel_name='ple.report.inv.bal.seventeen',
        string='Reporte de Estado de Situación financiera'
    )

    trial_balances_catalog_id = fields.Many2one(
        string='Cuenta contable',
        comodel_name='trial.balances.catalog'
    )
    name = fields.Char(
        string='Nombre de la cuneta contable',
        compute='calculate_name'
    )
    debit = fields.Char(
        string='Debe',
    )
    credit = fields.Char(
        string='Haber',
    )
    sequence = fields.Integer(
        string='Sequencia',
    )

    def calculate_name(self):
        for rec in self:
            data = rec.trial_balances_catalog_id
            rec.name = data.name
            rec.sequence = data.sequence
    






