from datetime import datetime
from odoo import api, fields, models


class StockRule(models.Model):
    _inherit = 'stock.rule'

    extra_pt = fields.Boolean(string="(%) Extra de PT")
