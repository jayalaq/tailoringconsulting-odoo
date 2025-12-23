from odoo import models, api, _, fields


class UoM(models.Model):
    _inherit = 'uom.uom'

    active_round = fields.Boolean(string='Round Up')
