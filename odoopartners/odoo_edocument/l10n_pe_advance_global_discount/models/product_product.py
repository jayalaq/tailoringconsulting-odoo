from odoo import api, fields, models


class ProductProduct(models.Model):
    _inherit = 'product.product'

    @api.onchange('l10n_pe_advance')
    def _onchange_l10n_pe_advance(self):
        for product in self:
            if product.l10n_pe_advance:
                product.global_discount = True
            else:
                product.global_discount = False
