from odoo import fields, models


class PosConfig(models.Model):
    _inherit = 'pos.config'

    automatic_print_electronic_invoice = fields.Boolean(
        string='Automatic Electronic Invoice Printing'
    )
    automatic_download_electronic_invoice = fields.Boolean(
        string='Automatic Electronic Invoice Download'
    )
