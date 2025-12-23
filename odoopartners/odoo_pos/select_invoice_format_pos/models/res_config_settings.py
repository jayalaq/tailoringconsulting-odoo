from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    pos_invoice_report_id = fields.Many2one(
        related='pos_config_id.invoice_report_id',
        string='Invoice Format',
        readonly=False
    )
