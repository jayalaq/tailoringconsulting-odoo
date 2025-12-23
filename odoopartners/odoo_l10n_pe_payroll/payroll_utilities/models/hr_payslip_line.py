from odoo import fields, models


class HrPayslipLine(models.Model):
    _inherit = 'hr.payslip.line'

    utilities = fields.Boolean(
        string='¿Aplica para utilidades?',
        related='salary_rule_id.utilities'
    )
