from odoo import api, fields, models

class AccountAccount(models.Model):
    _inherit = 'account.account'

    trial_balances_catalog_id = fields.Many2one(
        string='3.17 cuenta contable - SUNAT',
        comodel_name='trial.balances.catalog'
    )