from odoo import models, fields, api
from odoo.exceptions import ValidationError

class EpsEmployee(models.Model):
    _inherit = 'hr.employee'

    exists_eps = fields.Boolean(
        string='EPS',
        groups="hr.group_hr_user"
    )
    management_eps = fields.Many2one(
        comodel_name='eps.management',
        string='Poliza EPS',
        groups="hr.group_hr_user"
    )

    def update_management_eps_date(self):
        current_date = fields.Date.today()
        eps_existents = self.env['eps.management'].search([
            ('employeer_ids', 'in', self.id),
            ('star_date', '<=', current_date),
            ('finish_date', '>=', current_date)
        ])
        if eps_existents:
            self.management_eps = eps_existents[0].id
            self.exists_eps = True
        else:
            self.exists_eps = False
            self.management_eps = False

    @api.onchange('exists_eps')
    def _onchange_exists_eps(self):
        if not self.exists_eps:
            self.management_eps = False

    @api.model_create_multi
    def create(self, values):
        employee_ids = super(EpsEmployee, self).create(values)
        for employee in employee_ids:
            if employee.exists_eps and employee.management_eps:
                employee.management_eps.write({'employeer_ids': [(4, employee.id)]})
        return employee_ids

    def write(self,values):
        poliza_bef = self.management_eps
        result = super(EpsEmployee, self).write(values)
        if 'exists_eps' in values and 'management_eps' in values:
            for employee in self:
                if not employee.exists_eps or not employee.management_eps:
                    poliza_bef.write({'employeer_ids': [(3, employee.id)]})
                    employee.management_eps = False
                    employee.exists_eps = False
                elif employee.exists_eps and employee.management_eps:
                    employee.management_eps.write({'employeer_ids': [(4, employee.id)]})
        return result
