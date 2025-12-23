from odoo import api, fields, models, _


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    waste_mo_increment = fields.Integer(
        string='Margen Adicional (%)',
        default=0.0,
    )