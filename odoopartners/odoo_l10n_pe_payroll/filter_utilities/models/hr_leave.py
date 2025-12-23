from odoo import models, fields, api

class HrLeave(models.Model):
    _inherit = 'hr.leave'

    utilities = fields.Boolean(
        string='¿Aplica para utilidades?',
        related='holiday_status_id.utilities'
    )



