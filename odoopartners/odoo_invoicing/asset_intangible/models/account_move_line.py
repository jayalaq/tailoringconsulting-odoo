from odoo import api, fields, models


class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    asset_intangible_id = fields.Many2one(
        comodel_name='asset.intangible',
        string='Asset / Intangible'
    )