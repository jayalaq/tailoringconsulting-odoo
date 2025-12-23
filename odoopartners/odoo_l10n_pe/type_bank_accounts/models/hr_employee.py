from odoo import api, fields, models

class HrEmployeeTypeBankAccount(models.Model):
    _inherit = 'hr.employee'

    account_salary_bank = fields.Char(string='Cuenta Sueldo', readonly=True, compute='_compute_select_information_partner')
    type_salary_bank = fields.Char(string='Banco Sueldo', readonly=True, compute='_compute_select_information_partner')
    account_cts_bank = fields.Char(string='Cuenta CTS', readonly=True, compute='_compute_select_information_partner')
    type_cts_bank = fields.Char(string='Banco CTS', readonly=True, compute='_compute_select_information_partner')

    @api.depends('bank_account_id')
    def _compute_select_information_partner(self):
        for employee in self:
            res_partner_bank = employee.env['res.partner.bank'].search([('partner_id', '!=', False),('partner_id.id', '=', employee.work_contact_id.id)])
            account_salary_bank_employee = ''
            type_salary_bank_employee = ''
            account_cts_bank_employee = ''
            type_cts_bank_employee = ''
            for res in res_partner_bank:
                if res.acc_type == 'wage':
                    account_salary_bank_employee = res.acc_number
                    type_salary_bank_employee = res.bank_id.name
                if res.acc_type == 'cts':
                    account_cts_bank_employee = res.acc_number
                    type_cts_bank_employee = res.bank_id.name
            for result in employee:
                if account_salary_bank_employee != '':
                    result.account_salary_bank = account_salary_bank_employee
                else:
                    result.account_salary_bank = ''
                if type_salary_bank_employee != '':
                    result.type_salary_bank = type_salary_bank_employee
                else:
                    result.type_salary_bank = ''
                if account_cts_bank_employee != '':
                    result.account_cts_bank = account_cts_bank_employee
                else:
                    result.account_cts_bank = ''
                if type_cts_bank_employee != '':
                    result.type_cts_bank = type_cts_bank_employee
                else:
                    result.type_cts_bank = ''