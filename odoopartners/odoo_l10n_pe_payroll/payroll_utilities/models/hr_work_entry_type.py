from odoo import fields, models


class HrWorkEntryType(models.Model):
    _inherit = 'hr.work.entry.type'

    utilities = fields.Boolean(string='¿Aplica para utilidades?')
