from odoo import fields, models, api
from datetime import date

class PleInvBalLines(models.Model):
    _name = 'ple.report.inv.bal.line.12'
    _description = 'Reporte 3.12 - Líneas'

    report_id = fields.Many2one('ple.report.inv.bal.one')

    move = fields.Char()
    ple_correlative = fields.Char()
    l10n_latam_identification_type_id = fields.Char()
    vat = fields.Char()
    partner = fields.Char()
    balance = fields.Float()
    date = fields.Char()
    status = fields.Char()