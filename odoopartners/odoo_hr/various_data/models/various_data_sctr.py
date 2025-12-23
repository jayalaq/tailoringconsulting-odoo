from odoo import api, fields, models
from odoo.exceptions import ValidationError

class VariousDataSCTR(models.Model):
    _name = 'various.data.sctr'
    _description = 'Seguro Complementario de Trabajo de Riesgo'

    register_date = fields.Date(string='Fecha de registro')
    due_date = fields.Date(string='Fecha de vencimiento')
    pension_percent = fields.Float(string='Pensión %')
    health_percent = fields.Float(string='Salud %')
    pension_amount = fields.Float(string='Pensión Importe')
    health_amount = fields.Float(string='Salud Importe')
    name_id = fields.Many2one(
        comodel_name='res.partner',
        string='Nombre de la entidad',
        required=True
    )
    employee_ids = fields.One2many(
        comodel_name='hr.employee',
        inverse_name='sctr_id',
        string='Empleados'
    )
    sctr_name = fields.Char(string='Nombre de la póliza')

    @api.constrains('register_date', 'due_date')
    def _check_employee_overlap(self):
        for record in self:
            overlap_records = self.env['various.data.sctr'].search([
                ('id', '!=', record.id),
                ('name_id.employee_ids', 'in', record.name_id.employee_ids.ids),
                '|',
                ('register_date', '<=', record.register_date),
                ('register_date', '<=', record.due_date),
                '|',
                ('due_date', '>=', record.register_date),
                ('due_date', '>=', record.due_date),
            ])
            if overlap_records:
                raise ValidationError(
                    "Las fechas de esta póliza se superponen con otra póliza para uno o más empleados.")
                
    def name_get(self):
        res = []
        for _ in self:
            name = "%s" % (_.name_id.name)
            res.append((_.id, name))
        return res