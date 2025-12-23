from odoo import fields, models

class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    pension_sctr = fields.Boolean(
        string='SCTR',
        groups="hr.group_hr_user"
    )
    sctr_id = fields.Many2one(
        comodel_name='various.data.sctr',
        string='Poliza SCTR',
        groups="hr.group_hr_user"
    )
    sctr_name = fields.Char(
        string='Nombre de la Póliza',
        related='sctr_id.sctr_name',
        readonly=True
    )
