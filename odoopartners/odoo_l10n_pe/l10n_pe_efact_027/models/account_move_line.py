from odoo import fields, models


class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    reference_value_transportation_service = fields.Float(string='Valor referencial sobre el servicio de transporte',
                                                          default=0.10)
    reference_value_effective_load = fields.Float(string='Valor referencial sobre la carga efectiva', default=0.10)
    reference_value_on_nominal_payload = fields.Float(string='Valor referencial sobre la carga útil nominal',
                                                      default=0.10)
