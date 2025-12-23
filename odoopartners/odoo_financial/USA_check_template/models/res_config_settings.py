from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    type_bill = fields.Char(string='Type', config_parameter='USA.type_bill')