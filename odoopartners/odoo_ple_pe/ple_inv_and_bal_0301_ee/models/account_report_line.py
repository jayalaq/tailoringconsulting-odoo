from odoo import fields, models


class AccountReportLine(models.Model):
    _inherit = "account.report.line"

    eeff_ple_ids = fields.Many2one(
        'eeff.ple',
        string='3.1 Rubro ESF'
    )
