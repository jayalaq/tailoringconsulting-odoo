from odoo import fields, models

class AccountPaymentRegister(models.TransientModel):
    _inherit = 'account.payment.register'

    means_payment_id = fields.Many2one(default=False)