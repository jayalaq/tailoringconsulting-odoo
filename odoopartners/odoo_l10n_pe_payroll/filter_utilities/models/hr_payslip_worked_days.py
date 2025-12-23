from odoo import models, fields, api

class HrPayslipWorkedDays(models.Model):
    _inherit = 'hr.payslip.worked_days'

    utilities = fields.Boolean(
        string='¿Aplica para utilidades?',
        related='work_entry_type_id.utilities'
    )