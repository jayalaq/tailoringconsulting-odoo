from odoo import fields, models


class HrSalaryRule(models.Model):
    _inherit = 'hr.salary.rule'

    utilities = fields.Boolean(string='¿Aplica para utilidades?')
