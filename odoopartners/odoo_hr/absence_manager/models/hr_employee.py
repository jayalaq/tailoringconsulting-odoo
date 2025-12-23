from datetime import datetime
from dateutil.relativedelta import relativedelta
from odoo import models, fields, api

class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    attendance = fields.Boolean(
        string='¿Está obligado a marcar asistencia?',
        groups="hr.group_hr_user",
        default=True
    )

    @api.depends('attendance_ids')
    def _compute_last_attendance_id(self):
        for employee in self:
            record = self.env['hr.attendance'].search([
                ('employee_id', '=', employee.id),
                ('check_out', '=', False),
            ], limit=1)
            if not record:
                record = self.env['hr.attendance'].search([('employee_id', '=', employee.id)], limit=1)
            employee.last_attendance_id = record