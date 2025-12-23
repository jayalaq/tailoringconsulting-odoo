from odoo import api, models, fields


class ResPartner(models.Model):
    _inherit = 'res.partner'

    annexed_establishment = fields.Char(
        string='Establecimiento anexo',
        default='0000',
        help='Código asignado por SUNAT para el establecimiento anexo declarado en el RUC.'
    )

    @api.model
    def _get_view(self, view_id=None, view_type='form', **options):
        arch, view = super()._get_view(view_id, view_type, **options)
        if view_type in ('form'):
            tags = ['annexed_establishment']
            countries = [self.env.ref('base.pe')]
            arch, view = self._tags_invisible_per_country(arch, view, tags, countries)
        return arch, view
