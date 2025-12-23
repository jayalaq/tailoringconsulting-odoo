from odoo import fields, models

class HrPayslipWorkedDays(models.Model):
    _inherit = 'hr.payslip.worked_days'

    unpaid = fields.Boolean(
        string='Es no Pagada?',
        related='work_entry_type_id.unpaid'
    )
    is_social_benefits_license = fields.Boolean(
        string='¿Es licencia para Benef. Sociales?',
        related='work_entry_type_id.is_social_benefits_license'
    )
    is_benefits_license_absence = fields.Boolean(
        string='¿Es inasistencia para Benef. Sociales?',
        related='work_entry_type_id.is_benefits_license_absence'
    )
    is_calc_own_rule = fields.Boolean(
        string='¿Es calculado por su propia regla?',
        related='work_entry_type_id.is_calc_own_rule'
    )