from odoo import fields, models


class PosConfigInherit(models.Model):
    _inherit = "pos.config"

    order_barcode = fields.Boolean("Order Barcode")
    barcode_selection = fields.Selection(
        selection=[
            ("qrcode", "QRCode"), 
            ("barcode", "Barcode")
        ], 
        string="Code"
    )
    invoice_number = fields.Boolean("Invoice Number")
    customer_details = fields.Boolean("Customer Details")
    customer_name = fields.Boolean("Customer Name")
    customer_address = fields.Boolean("Customer Address")
    customer_mobile = fields.Boolean("Customer Mobile")
    customer_phone = fields.Boolean("Customer Phone")
    order_number = fields.Boolean("Order Number")
    customer_email = fields.Boolean("Customer Email")
    customer_vat = fields.Boolean("Customer Vat")
    customer_name_custom_title = fields.Char("Customer Name Custom Title")
    customer_address_custom_title = fields.Char("Customer Address Custom Title")
    customer_mobile_custom_title = fields.Char("Customer Mobile Custom Title")
    customer_phone_custom_title = fields.Char("Customer Phone Custom Title")
    customer_email_custom_title = fields.Char("Customer Email Custom Title")
    customer_vat_custom_title = fields.Char("Customer Vat Custom Title")
    font_size = fields.Float(digits=(10, 2), default=12)
    bold_format = fields.Boolean()


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    order_barcode = fields.Boolean(
        related="pos_config_id.order_barcode", 
        readonly=False,
    )
    barcode_selection = fields.Selection(
        related="pos_config_id.barcode_selection", 
        readonly=False,
    )
    invoice_number = fields.Boolean(
        related="pos_config_id.invoice_number", 
        readonly=False,
    )
    customer_details = fields.Boolean(
        related="pos_config_id.customer_details", 
        readonly=False,
    )
    customer_name = fields.Boolean(
        related="pos_config_id.customer_name", 
        readonly=False,
    )
    customer_address = fields.Boolean(
        related="pos_config_id.customer_address", 
        readonly=False,
    )
    customer_mobile = fields.Boolean(
        related="pos_config_id.customer_mobile", 
        readonly=False,
    )
    customer_phone = fields.Boolean(
        related="pos_config_id.customer_phone", 
        readonly=False,
    )
    order_number = fields.Boolean(
        related="pos_config_id.order_number", 
        readonly=False,
    )
    customer_email = fields.Boolean(
        related="pos_config_id.customer_email", 
        readonly=False,
    )
    customer_vat = fields.Boolean(
        related="pos_config_id.customer_vat", 
        readonly=False,
    )
    customer_name_custom_title = fields.Char(
        related="pos_config_id.customer_name_custom_title", 
        readonly=False,
    )
    customer_address_custom_title = fields.Char(
        related="pos_config_id.customer_address_custom_title", 
        readonly=False,
    )
    customer_mobile_custom_title = fields.Char(
        related="pos_config_id.customer_mobile_custom_title", 
        readonly=False,
    )
    customer_phone_custom_title = fields.Char(
        related="pos_config_id.customer_phone_custom_title", 
        readonly=False,
    )
    customer_email_custom_title = fields.Char(
        related="pos_config_id.customer_email_custom_title", 
        readonly=False,
    )
    customer_vat_custom_title = fields.Char(
        related="pos_config_id.customer_vat_custom_title", 
        readonly=False,
    )
    font_size = fields.Float(
        related="pos_config_id.font_size", 
        readonly=False,
    )
    bold_format = fields.Boolean(
        related="pos_config_id.bold_format",
        readonly=False,
    )
