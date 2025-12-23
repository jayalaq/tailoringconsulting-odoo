from odoo import models, fields


class AccountAccount(models.Model):
    _inherit = 'account.account'

    adjustment_rate = fields.Float('Tasa de Ajuste', digits=(5, 12))
