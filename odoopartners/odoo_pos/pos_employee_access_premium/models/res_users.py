from odoo import models, fields


HR_WRITABLE_FIELDS = [
    'pos_access_close',
    'pos_access_make_payments',
    'pos_access_make_refunds',
    'pos_access_make_discounts',
    'pos_access_change_price',
    'pos_access_delete_orders',
    'pos_access_delete_order_lines',
    'pos_access_decrease_quantity_order_lines',
    'pos_access_cash_in_out',
    'pos_access_product_information'
]


class ResUsers(models.Model):
    _inherit = 'res.users'

    pos_access_close = fields.Boolean(
        related='employee_id.pos_access_close',
        readonly=False,
        related_sudo=False
    )
    pos_access_make_payments = fields.Boolean(
        related='employee_id.pos_access_make_payments',
        readonly=False,
        related_sudo=False
    )
    pos_access_make_refunds = fields.Boolean(
        related='employee_id.pos_access_make_refunds',
        readonly=False,
        related_sudo=False
    )
    pos_access_make_discounts = fields.Boolean(
        related='employee_id.pos_access_make_discounts',
        readonly=False,
        related_sudo=False
    )
    pos_access_change_price = fields.Boolean(
        related='employee_id.pos_access_change_price',
        readonly=False,
        related_sudo=False
    )
    pos_access_delete_orders = fields.Boolean(
        related='employee_id.pos_access_delete_orders',
        readonly=False,
        related_sudo=False
    )
    pos_access_delete_order_lines = fields.Boolean(
        related='employee_id.pos_access_delete_order_lines',
        readonly=False,
        related_sudo=False
    )
    pos_access_decrease_quantity_order_lines = fields.Boolean(
        related='employee_id.pos_access_decrease_quantity_order_lines',
        readonly=False,
        related_sudo=False
    )
    pos_access_cash_in_out = fields.Boolean(
        related='employee_id.pos_access_cash_in_out',
        readonly=False,
        related_sudo=False
    )
    pos_access_product_information = fields.Boolean(
        related='employee_id.pos_access_product_information',
        readonly=False,
        related_sudo=False
    )

    @property
    def SELF_READABLE_FIELDS(self):
        return super().SELF_READABLE_FIELDS + HR_WRITABLE_FIELDS

    @property
    def SELF_WRITEABLE_FIELDS(self):
        return super().SELF_WRITEABLE_FIELDS + HR_WRITABLE_FIELDS
