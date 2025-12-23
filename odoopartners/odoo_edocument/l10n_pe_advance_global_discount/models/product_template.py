from odoo import api, fields, models


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    l10n_pe_advance = fields.Boolean(
        string='Anticipo'
    )

    @api.onchange('l10n_pe_advance')
    def _onchange_l10n_pe_advance(self):
        for product in self:
            if product.l10n_pe_advance:
                product.global_discount = True
            else:
                product.global_discount = False
