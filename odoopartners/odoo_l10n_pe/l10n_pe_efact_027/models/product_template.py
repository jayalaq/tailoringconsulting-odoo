from odoo import fields, models


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    service_detail = fields.Char(string='Detalle del servicio')