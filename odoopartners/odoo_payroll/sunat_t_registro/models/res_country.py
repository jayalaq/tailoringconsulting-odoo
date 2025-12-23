from odoo import api, fields, models

class ResCountry(models.Model):
    _inherit = 'res.country'

    cod_pas_only = fields.Char(string='Código sólo para pasaporte')
    nacionality_code_rc = fields.Char(string='Código de Nacionalidad')