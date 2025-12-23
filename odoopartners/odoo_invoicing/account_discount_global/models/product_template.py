from odoo import fields, models


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    global_discount = fields.Boolean(string='Descuento Global')
