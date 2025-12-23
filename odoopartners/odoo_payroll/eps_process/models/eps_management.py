from odoo import models, fields, api
from odoo.exceptions import ValidationError

class EpsManagement(models.Model):
    _name = "eps.management"
    _description = "EPS management"

    display_name = fields.Char(
        compute='_compute_display_name'
    )
    star_date = fields.Date(
        string='Fecha de inicio',
        required=True
    )
    finish_date = fields.Date(
        string='Fecha de finalización',
        required=True
    )
    entity = fields.Char(
        string='Entidad',
        required=True
    )
    partner_id = fields.Many2one(
        comodel_name='res.partner',
        string='Entidad',
        required=True
    )
    insurance = fields.Char(
        string='N° de poliza'
    )
    rate_employer = fields.Float(
        string='Porcentaje Empleador'
    )
    amount_employer = fields.Float(
        string='Importe Empleador'
    )
    rate_worker = fields.Float(
        string='Porcentaje Trabajador'
    )
    amount_worker = fields.Float(
        string='Importe Trabajador'
    )
    employeer_ids = fields.Many2many(
        comodel_name='hr.employee',
        string='Empleados'
    )
    _writing_employees = fields.Boolean(
        default=False,
        readonly=False
    )

    @api.depends('entity','insurance')
    def _compute_display_name(self):
        for rec in self:
            if rec.entity and rec.insurance:
                rec.display_name = '%s-%s' % (rec.entity, rec.insurance)
            else:
                rec.display_name = 'Entidad-N° de poliza'

    @api.onchange('partner_id')
    def _on_change_entity(self):
        self.entity = self.partner_id.display_name

    def write(self,values):
        employeers_to_remove_origin = self._origin.employeer_ids
        result = super(EpsManagement, self).write(values)
        if 'employeer_ids' in values and not getattr(self, '_writing_employees', False):
            self._writing_employees = True
            employees_to_add = self.mapped('employeer_ids')
            employees_to_remove = set(employeers_to_remove_origin.ids) - set(self.employeer_ids.ids)
            for employee in employees_to_add:
                employee.write({'management_eps': self.id, 'exists_eps': True})
            for employee in employees_to_remove:
                removed_employee = self.env['hr.employee'].search([('id', '=', employee)])
                removed_employee.write({'management_eps': False, 'exists_eps': False})
                removed_employee.exists_eps = False
            self._writing_employees = False
        return result


    @api.constrains('employeer_ids', 'star_date', 'finish_date')
    def _check_employee_conflicts(self):
        for insurance in self:
            for employee in insurance.employeer_ids:
                conflicting_insurances_up = self.env['eps.management'].search([
                    ('id', '!=', insurance.id),
                    ('employeer_ids', 'in', employee.id),
                    '|',
                    ('finish_date', '>=', insurance.finish_date),
                    ('finish_date', '>=', insurance.star_date)
                ])
                conflicting_insurances_down=self.env['eps.management'].search([
                    ('id', '!=', insurance.id),
                    ('employeer_ids', 'in', employee.id),
                    '|',
                    ('finish_date', '<=', insurance.finish_date),
                    ('finish_date', '<=', insurance.star_date)
                ])
                if conflicting_insurances_up and conflicting_insurances_down:
                    raise ValidationError(f"El empleado {employee.name} tiene conflictos de fechas con otros seguros.")
