from odoo import api, fields, models

class TopeAFP(models.Model):
    _name = 'tope.afp'
    _description = 'Tope AFP'

    date_from = fields.Date(
        string='Desde',
        required=True
    )
    date_to = fields.Date(
        string='Hasta',
        required=True
    )
    top = fields.Float(string='Tope')
    
    def _compute_display_name(self):
        for rec in self:
            rec.display_name = '[%s - %s] %s' % (rec.date_from or '', rec.date_to or '', rec.top)
