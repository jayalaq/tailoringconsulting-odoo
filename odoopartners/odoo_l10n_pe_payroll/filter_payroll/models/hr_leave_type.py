from odoo import fields, models

class HrLeaveType(models.Model):
    _inherit = 'hr.leave.type'

    unpaid = fields.Boolean(related='work_entry_type_id.unpaid', default=None)
    is_social_benefits_license = fields.Boolean(
        string='¿Es Licencia para Benef. Sociales?',
        related='work_entry_type_id.is_social_benefits_license'
    )
    is_benefits_license_absence = fields.Boolean(
        string='¿Es Inasistencia para Benef. Sociales?',
        related='work_entry_type_id.is_benefits_license_absence'
    )
    is_calc_own_rule = fields.Boolean(
        string='¿Es calculado por su propia regla?',
        related='work_entry_type_id.is_calc_own_rule'
    )
