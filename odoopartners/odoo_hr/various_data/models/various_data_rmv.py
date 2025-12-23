from odoo import fields, models

class VariousDataRMV(models.Model):
    _name = 'various.data.rmv'
    _description = 'Remuneracion minima vital'

    register_date = fields.Date(string='Fecha de registro')
    due_date = fields.Date(string='Fecha de vencimiento')
    rmv_amount = fields.Float(string='Importe RMV')
    af_amount = fields.Float(string='Importe AF')
    is_active = fields.Boolean(string='Activo')