from odoo import api, fields, models

class HrContract(models.Model):
    _inherit = 'hr.contract'

    special_situation_id = fields.Many2one(
        comodel_name='special.situation',
        string='Situación Especial'
    )
    payment_type_id = fields.Many2one(
        comodel_name='payment.type',
        string='Tipo de pago'
    )
    variable_payment_id = fields.Many2one(
        comodel_name='variable.payment',
        string='Remuneración Variable'
    )
    schedule_pay_conditions = fields.Many2one(
        comodel_name='payment.period',
        related='structure_type_id.default_struct_id.schedule_pay_conditions'
    )

