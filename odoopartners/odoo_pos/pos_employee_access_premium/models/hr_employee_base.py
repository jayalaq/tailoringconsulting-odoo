from odoo import fields, models


class HrEmployeeBase(models.AbstractModel):
    _inherit = 'hr.employee.base'

    pos_access_close = fields.Boolean(
        string='Access Close POS',
        default=True,
        copy=False
    )
    pos_access_make_payments = fields.Boolean(
        string='Access Make Payments',
        default=True,
        copy=False
    )
    pos_access_make_refunds = fields.Boolean(
        string='Access Make Refunds',
        default=True,
        copy=False
    )
    pos_access_make_discounts = fields.Boolean(
        string='Access Make Discounts',
        default=True,
        copy=False
    )
    pos_access_change_price = fields.Boolean(
        string='Access Change Price',
        default=True,
        copy=False
    )
    pos_access_delete_orders = fields.Boolean(
        string='Access Delete Orders',
        default=True,
        copy=False
    )
    pos_access_delete_order_lines = fields.Boolean(
        string='Access Delete Order Lines',
        default=True,
        copy=False
    )
    pos_access_decrease_quantity_order_lines = fields.Boolean(
        string='Access Decrease Quantity Order Lines',
        default=True,
        copy=False
    )
    pos_access_cash_in_out = fields.Boolean(
        string='Access Cash In/Out',
        default=True,
        copy=False
    )
    pos_access_product_information = fields.Boolean(
        string='Access Product Information',
        default=True,
        copy=False
    )
