from odoo import models


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    def _create_recurring_invoice(self, batch_size=30):
        invoices = super()._create_recurring_invoice(batch_size)
        for invoice in invoices:
            invoice = invoice.with_company(invoice.company_id)
            invoice.with_context(tracking_disable=True)._get_change_account()
        return invoices
