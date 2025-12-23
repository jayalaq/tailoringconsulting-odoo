from odoo import fields, models


class AccountPayment(models.Model):
    _inherit = "account.payment"

    means_payment_id = fields.Many2one(default=False)

