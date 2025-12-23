from odoo import fields, models


class PosOrder(models.Model):
    _inherit = 'pos.order'

    account_move_rel_name = fields.Char(
        string='Invoice/Bill Number',
        related='account_move.name',
        store=True
    )
    account_move_rel_document_type = fields.Char(
        string='Invoice/Bill Document Type',
        related='account_move.l10n_latam_document_type_id.name',
        store=True
    )
    account_move_rel_invoice_date = fields.Date(
        string='Invoice/Bill Date',
        related='account_move.invoice_date',
        store=True
    )

    def _export_for_ui(self, order):
        order_list = super()._export_for_ui(order)
        order_list['account_move_rel_name'] = order.account_move_rel_name
        order_list['account_move_rel_document_type'] = order.account_move_rel_document_type
        order_list['account_move_rel_invoice_date'] = order.account_move_rel_invoice_date
        return order_list
