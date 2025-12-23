from odoo import fields, models


class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    partner_concept_ids = fields.Many2many(
        comodel_name='hr.partner.concept',
        relation='hr_employee_hr_partner_concept_rel',
        string='Reglas Salariales',
        groups='hr.group_hr_user'
    )
