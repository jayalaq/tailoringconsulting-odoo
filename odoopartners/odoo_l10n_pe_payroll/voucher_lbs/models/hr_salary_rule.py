from odoo import api, fields, models


class HrSalaryRule(models.Model):
    _inherit = 'hr.salary.rule'

    section_lbs_ids = fields.Many2many(
        comodel_name='section.lbs',
        string='Sección de Liquidación'
    )
