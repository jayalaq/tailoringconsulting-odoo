from odoo import models


class SaleAdvancePaymentInv(models.TransientModel):
    _inherit = 'sale.advance.payment.inv'

    def _create_invoices(self, sale_orders):
        move = super()._create_invoices(sale_orders)
        move.with_context(tracking_disable=True)._get_change_account()
        return move
