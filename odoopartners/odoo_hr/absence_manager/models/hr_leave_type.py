from datetime import datetime
from dateutil.relativedelta import relativedelta
from odoo import models, fields, api

class HrLeaveType(models.Model):
    _inherit = 'hr.leave.type'

    code = fields.Char('Code')
    