from odoo import models, fields, api


class HrContract(models.Model):
    _inherit = 'hr.contract'

    labor_regime_id = fields.Many2one(
        comodel_name="employee.regime",
        string='Régimen Laboral'
    )
    labor_condition_id = fields.Many2one(
        comodel_name='type.contract',
        string='Condición laboral'
    )
    maximum_working_day = fields.Boolean(
        string='Jornada de trabajo máxima'
    )
    atypical_cumulative_day = fields.Boolean(
        string='Jornada atípica o acumulativa'
    )
    nocturnal_schedule = fields.Boolean(
        string='Trabajo en horario nocturno'
    )
    unionized = fields.Boolean(
        string='Sindicalizado'
    )
    is_practitioner = fields.Boolean(
        string='¿Es practicante?'
    )
    work_occupation_id = fields.Many2one(
        comodel_name="work.occupation",
        string='Ocupación de trabajo'
    )

