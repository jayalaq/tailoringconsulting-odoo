from odoo import fields, models


class PleInvBalLines(models.Model):
    _name = 'ple.report.inv.bal.line.07'
    _description = 'Estado de Situación financiera - Líneas'

    product_id = fields.Integer(string='Producto')
    period = fields.Char(string="Periodo")
    stock_catalog = fields.Char(string='Código de catálogo')
    stock_type = fields.Char(string='Tipo de Existencia')
    default_code = fields.Char(string="Código propio de la existencia")
    code_catalog_used = fields.Char(string="Código catalogo utilizado")
    unspsc_code = fields.Char(string="UNSPSC Codigo") #antes unspc_code_id
    product_description = fields.Char(string='Descripcion de existencia')
    product_udm = fields.Char(string='Código de la unidad de medida')
    property_cost_method = fields.Char("Código del método de valuación")
    quantity_product_hand = fields.Float(string='Cantidad de existencia')
    standard_price = fields.Float(string='Costo unitario')
    total = fields.Float(string='Costo Total')
    # aml_id = fields.Integer(string='aml valuation')
    # company_id = fields.Integer(string='Company id')
    # last_date = fields.Date(string="Dia del ultimo registro ")
    ple_report_inv_val_07_id = fields.Many2one(
        comodel_name='ple.report.inv.bal.07',
        string='Reporte de Estado de Situación financiera'
    )
