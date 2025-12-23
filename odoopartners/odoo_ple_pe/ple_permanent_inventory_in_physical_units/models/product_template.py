from odoo import api, models, fields, api
from odoo.tools import float_round

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    stock_catalog = fields.Selection(
        selection=[
            ('1', "[1] NACIONES UNIDAS (UNSPSC)"),
            ('3', "[3] GS1 (EAN-UCC)"),
            ('9', "[9] Otros")],
        string="Catálogo de existencia",
        help='Este código se usa en los libros PLE de inventario permanente y se valida con la tabla 13 del anexo 3'
    )
    stock_type = fields.Selection(
        selection=[
            ('01', "[01] Mercadería"),
            ('02', "[02] Productos terminados"),
            ('03', "[03] Materias Primas"),
            ('04', "[04] Envases"),
            ('05', "[05] Materiales Auxiliares"),
            ('06', "[06] Suministros"),
            ('07', "[07] Repuestos"),
            ('08', "[08] Enbalajes"),
            ('09', "[09] SubProductos"),
            ('10', "[10] Desechos y desperdicios"),
            ('91', "[91] Otros 1"),
            ('92', "[92] Otros 2"),
            ('93', "[93] Otros 3"),
            ('94', "[94] Otros 4"),
            ('95', "[95] Otros 5"),
            ('96', "[96] Otros 6"),
            ('97', "[97] Otros 7"),
            ('98', "[98] Otros 8"),
            ('99', "[99] Otros"),
        ],
        string="Tipo de existencia",
        help='Este código se usa en los libros PLE de inventario permanente y se valida con la tabla 13 del anexo 3'
    )

    @api.model
    def _get_view(self, view_id=None, view_type='form', **options):
        arch, view = super()._get_view(view_id, view_type, **options)
        if view_type in ('form'):
            tags = [('field', 'stock_catalog'), ('field', 'stock_type')]
            arch, view = self.env['res.partner']._tags_invisible_per_country(arch, view, tags, [self.env.ref('base.pe')])
        return arch, view