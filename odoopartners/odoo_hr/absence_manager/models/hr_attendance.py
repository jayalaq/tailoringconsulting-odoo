from datetime import datetime
from dateutil.relativedelta import relativedelta
from odoo import models, fields, api

class HrAttendance(models.Model):
    _inherit = 'hr.attendance'

    leave_id = fields.Many2one(
        comodel_name='hr.leave',
        string='Ausencia'
    )
    holiday_status_id = fields.Many2one(
        comodel_name="hr.leave.type",
        string="Tipo de Ausencia",
        readonly=True
    )