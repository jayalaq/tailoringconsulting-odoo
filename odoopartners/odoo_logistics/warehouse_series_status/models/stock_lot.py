from odoo import models, fields


class StockLot(models.Model):
    _inherit = 'stock.lot'

    status = fields.Many2one(
        comodel_name='stock.production.lot.status',
        string='Status',
        help='Este campo se aprovecha mejor, cuando se trata de productos que utilizan el método de seguimiento de serie, porque nos ayuda a identificar el '
             'estatus del producto relacionado a la serie. Cuando se establece un status en una transferencia o ajuste de inventario, se almacena el valor en este campo.'
    )
