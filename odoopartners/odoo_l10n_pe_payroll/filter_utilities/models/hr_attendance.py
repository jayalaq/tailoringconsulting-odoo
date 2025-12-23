from odoo import models, fields, api

class HrAttendance(models.Model):
    _inherit = 'hr.attendance'

    utilities = fields.Boolean(
        string='¿Aplica para utilidades?',
        related='holiday_status_id.utilities'
    )