from odoo import api, fields, models

class HrPayrollStructureType(models.Model):
    _inherit = 'hr.payroll.structure.type'

    default_schedule_pay_conditions = fields.Many2one(
        comodel_name='payment.period',
        string='Pago programado predeterminado',
        default=lambda self: self.env.ref('payment_conditions.payment_period_1', False),
        help="Defines the frequency of the wage payment."
    )