from odoo import api, fields, models, _
from odoo.exceptions import UserError


class PurchaseOrderLine(models.Model):
    """ Adds product image to purchase order line """

    _inherit = 'purchase.order.line'

    product_image = fields.Binary(
        related="product_id.image_1920",
        string="Image",
        help='For getting product image '
             'to purchase order line')

    @api.onchange('order_id')
    def onchange_order_id(self):
        """ Prevents adding lines to orders in locked, canceled, or purchased states """
        
        if self.order_id.state in ['cancel', 'done', 'purchase']:
            raise UserError(_("Cannot modify order in canceled, locked, or purchased state"))
