from odoo import models, fields, api

class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    contract_id = fields.Many2one(
        comodel_name='hr.contract',
        string='Current Contract',
        help='Current contract of the employee',
        groups="hr.group_hr_user",
        domain="[('company_id', '=', company_id),('employee_id', '=', id)]"
    )
    service_start_date = fields.Date(
        string='Start Date',
        store=True
    )
    service_termination_date = fields.Date(
        string='Termination Date',
        store=True
    )

    @api.depends('contract_id', 'contract_id.date_end')
    def compute_contract_date(self):
        for rec in self:
            if rec.contract_id:
                rec.service_termination_date = rec.contract_id.date_end

    @api.onchange('contract_id')
    def _onchange_contract_id(self):
        for rec in self:
            if rec.contract_id:
                rec.service_termination_date = rec.contract_id.date_end

    def _get_contract_filter(self):
        self.ensure_one()
        return [('employee_id', '=', self.id), ('state', 'in', self._get_service_contract_states())]

    @api.model
    def _get_service_contract_states(self):
        return ['open', 'pending', 'close']

    @api.model
    def _action_update_service_duration(self):
        employees = self.search([])
        employees.compute_contract_date()
