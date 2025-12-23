from dateutil.relativedelta import relativedelta
from odoo import api, fields, models


class HrEmployeeRelative(models.Model):
    _name = 'hr.employee.relative'
    _description = 'HR Employee Relative'

    name = fields.Char(
        string='Nombre',
        required=True
    )
    job = fields.Char(
        string='Profesión'
    )
    phone_number = fields.Char(
        string='Teléfono'
    )
    date_of_birth = fields.Date(
        string='Fecha de nacimiento'
    )
    gender = fields.Selection(
        string='Género',
        selection=[
            ('masculino', 'Masculino'),
            ('femenino', 'Femenino'),
            ('otro', 'Otro')
        ]
    )
    notes = fields.Text(
        string='Notas'
    )
    age = fields.Integer(
        string='Edad',
        compute='_compute_age'
    )
    employee_id = fields.Many2one(
        string='Empleado',
        comodel_name='hr.employee'
    )
    relation_id = fields.Many2one(
        string='Parentesco',
        comodel_name='hr.employee.relative.relation',
        required=True
    )
    partner_id = fields.Many2one(
        string='Contacto',
        comodel_name='res.partner',
        domain="[('is_company', '=', False), ('type', '=', 'contact')]",
    )

    @api.depends('date_of_birth')
    def _compute_age(self):
        for relative in self:
            age = 0
            if relative.date_of_birth:
                age = relativedelta(fields.Date.today(), relative.date_of_birth).years
            relative.age = age

    @api.onchange('partner_id')
    def _onchange_partner_id(self):
        if self.partner_id:
            self.name = self.partner_id.display_name
        else:
            self.name = False
