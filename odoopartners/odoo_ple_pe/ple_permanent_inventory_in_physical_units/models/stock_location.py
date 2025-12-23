from odoo import api, models, fields, _
from odoo.tools import float_round


class StockLocation(models.Model):
    _inherit = 'stock.location'

    correlative = fields.Integer(
        string='Correlativo'
    )
    storehouse_id = fields.Many2one(
        comodel_name='stock.warehouse', 
        string="Almacen"
    )

    @api.model
    def _get_view(self, view_id=None, view_type='form', **options):
        arch, view = super()._get_view(view_id, view_type, **options)
        if view_type in ('form'):
            tags = [('field', 'correlative')]
            arch, view = self.env['res.partner']._tags_invisible_per_country(arch, view, tags, [self.env.ref('base.pe')])
        return arch, view