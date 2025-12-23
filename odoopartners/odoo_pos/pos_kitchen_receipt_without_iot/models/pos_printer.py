from odoo import models, fields, api


class PosPrinter(models.Model):
    _inherit = 'pos.printer'
    
    printer_type = fields.Selection(
        selection_add=[
            ('web_printer', 'Using the web printer')
        ]
    )
