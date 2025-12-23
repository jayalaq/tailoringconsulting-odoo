from odoo import fields, models

class VariousDataUIT(models.Model):
    _name = 'various.data.uit'
    _description = 'Unidad Impositiva Tributaria'

    register_date = fields.Date(string='Fecha de registro')
    due_date = fields.Date(string='Fecha de vencimiento')
    uit_amount = fields.Float(string='Importe')
    is_active = fields.Boolean(string='Activo')