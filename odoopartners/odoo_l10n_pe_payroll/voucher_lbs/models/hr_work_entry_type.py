from odoo import api, fields, models


class HrWorkEntryType(models.Model):
    _inherit = 'hr.work.entry.type'

    section_lbs_ids = fields.Many2many(
        comodel_name='section.lbs',
        string='Sección de Liquidación'
    )
