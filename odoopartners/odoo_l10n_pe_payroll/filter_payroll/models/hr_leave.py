from odoo import fields, models

class HrLeave(models.Model):
    _inherit = 'hr.leave'

    unpaid = fields.Boolean(
        string='Is Unpaid',
        related='holiday_status_id.unpaid'
    )
    is_social_benefits_license = fields.Boolean(
        string='¿Es Licencia para Benef. Sociales?',
        related='holiday_status_id.is_social_benefits_license'
    )
    is_benefits_license_absence = fields.Boolean(
        string='¿Es Inasistencia para Benef. Sociales?',
        related='holiday_status_id.is_benefits_license_absence'
    )
    is_calc_own_rule = fields.Boolean(
        string='¿Es calculado por su propia regla?',
        related='holiday_status_id.is_calc_own_rule'
    )
    code_holiday = fields.Char(
        string='Código ausencia',
        related='holiday_status_id.code'
    )