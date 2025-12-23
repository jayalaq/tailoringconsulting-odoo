from odoo import models


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    def action_view_invoice(self, invoices=False):
        if not invoices:
            self.invalidate_model(['invoice_ids'])
            invoices = self.invoice_ids
        for invoice in invoices:
            invoice.with_context(tracking_disable=True)._get_change_account()
        return super().action_view_invoice(invoices)
