from odoo import fields, models


class ResourceCalendar(models.Model):
    _inherit = 'resource.calendar'

    tolerance_time = fields.Integer(
        string='Tiempo de tolerancia'
    )
