from odoo import fields, models, api


class AccountPayment(models.Model):
    _inherit = "account.payment"

    def _get_default_means_payment(self):
        means_payment_id = self.env['payment.methods.codes'].search([('code', '=', '003')])
        if means_payment_id:
            return means_payment_id.id

    means_payment_id = fields.Many2one(
        comodel_name='payment.methods.codes',
        string="Medio de pago - libro de bancos",
        default=lambda self: self._get_default_means_payment()
    )