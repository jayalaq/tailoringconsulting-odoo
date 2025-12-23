from odoo import fields, models

class VariousDataSIS(models.Model):
    _name = 'various.data.sis'
    _description = 'Seguro Integral de Salud'

    register_date = fields.Date(string='Fecha de registro')
    due_date = fields.Date(string='Fecha de vencimiento')
    sis_amount = fields.Float(string='Importe')
    is_active = fields.Boolean(string='Activo')