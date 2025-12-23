from odoo import fields, models


class PosConfig(models.Model):
    _inherit = 'pos.config'

    invoice_report_id = fields.Many2one(
        comodel_name='ir.actions.report',
        string='Invoice Format',
        domain='[("model", "=", "account.move")]',
        default=lambda self: self.env.ref('account.account_invoices')
    )
