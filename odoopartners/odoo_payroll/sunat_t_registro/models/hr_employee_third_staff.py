from odoo import api, fields, models

class HrEmployeThirdStaff(models.Model):
    _name = 'hr.employee.third.staff'
    _description = 'Empleados Personal de Tercero'

    name = fields.Char(string='Nombre')
    contact_id = fields.Many2one('res.partner', string='Contacto')
    type_identification_id = fields.Many2one(
        comodel_name="l10n_latam.identification.type",
        string='Tipo de doc.',
        groups="hr.group_hr_user"
    )
    document_country_id = fields.Many2one(
        comodel_name="res.country",
        string='País emisor del documento',
        groups="hr.group_hr_user"
    )
    identification_id = fields.Char(string='N° identificación')
    date_from = fields.Datetime(string='Desde')
    date_to = fields.Datetime(string='Hasta')
    sctr = fields.Selection(string='SCTR Pensión', selection=[
        ('01', 'ONP'),
        ('02', 'Seguro Privado'),
    ])
    registered_t_register = fields.Boolean(string='Registrado en T-Registro')
    employee_id = fields.Many2one(comodel_name='third.staff')