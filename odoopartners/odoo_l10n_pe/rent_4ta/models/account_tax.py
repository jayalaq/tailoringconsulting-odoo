from odoo import models, api, fields
from odoo.exceptions import ValidationError
from odoo.osv import expression

class AccountTax(models.Model):
    _inherit = 'account.tax'

    @api.constrains('company_id', 'name', 'type_tax_use', 'tax_scope', 'country_id')
    def _constrains_name(self):
        """
        Sobreescribe la restricción para que el nombre del impuesto no tenga que ser único entre diferentes compañías.
        """
        for taxes in self:
            # Crear dominios sin validar la unicidad del nombre entre compañías
            domains = []
            for tax in taxes:
                if tax.type_tax_use != 'none':
                    domains.append([
                        ('company_id', '=', tax.company_id.id),  # Permitir duplicados en diferentes compañías
                        ('name', '=', tax.name),
                        ('type_tax_use', '=', tax.type_tax_use),
                        ('tax_scope', '=', tax.tax_scope),
                        ('country_id', '=', tax.country_id.id),
                        ('id', '!=', tax.id),
                    ])
            if duplicates := self.search(expression.OR(domains)):
                raise ValidationError(
                    _("Tax names must be unique within the same company!")
                    + "\n" + "\n".join(_(
                        "- %(name)s in %(company)s",
                        name=duplicate.name,
                        company=duplicate.company_id.name,
                    ) for duplicate in duplicates)
                )
