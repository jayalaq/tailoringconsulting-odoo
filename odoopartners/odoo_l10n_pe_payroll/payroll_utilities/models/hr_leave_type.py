from odoo import fields, models


class HrLeaveType(models.Model):
    _inherit = 'hr.leave.type'

    utilities = fields.Boolean(
        string='¿Aplica para utilidades?',
        related='work_entry_type_id.utilities'
    )
