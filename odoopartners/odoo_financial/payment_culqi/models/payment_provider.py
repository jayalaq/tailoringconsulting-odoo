from odoo import models, fields, api, _


class PaymentProvider(models.Model):
    _inherit = "payment.provider"

    code = fields.Selection(
        selection_add=[("culqi", "Culqi")], 
        ondelete={"culqi": "set default"}
    )
    culqi_public_key = fields.Char(
        string="Llave pública", 
        required_if_provider="culqi", 
        groups="base.group_system"
    )
    culqi_private_key = fields.Char(
        string="Llave privada", 
        required_if_provider="culqi", 
        groups="base.group_system"
    )

    @api.model
    def _get_compatible_providers(self, *args, is_validation=False, **kwargs):
        """Override of payment to unlist Culqi providers for validation operations."""
        providers = super()._get_compatible_providers(
            *args, is_validation=is_validation, **kwargs
        )

        if is_validation:
            providers = providers.filtered(lambda p: p.code != "culqi")

        return providers

    def _get_supported_currencies(self):
        """Override of `payment` to return the supported currencies."""
        supported_currencies = super()._get_supported_currencies()
        if self.code == "culqi":
            supported_currencies = supported_currencies.filtered(
                lambda c: c.name in ("PEN", "USD")
            )
        return supported_currencies
