from odoo import models, fields, api, _
from odoo.tools import float_round, date_utils
from odoo.tools.misc import format_date
from dateutil.relativedelta import relativedelta
from odoo.exceptions import UserError
from collections import defaultdict
from datetime import datetime

class HrPayslip(models.Model):
    _inherit = 'hr.payslip'

    def action_remove_zeros(self):
        for rec in self:
            salary_calculation_lines = rec.line_ids.filtered(lambda x: x.amount == 0)
            salary_calculation_lines.unlink()

            days_lines = rec.worked_days_line_ids.filtered(lambda x: x.number_of_days == 0)
            days_lines.unlink()
            input_lines = rec.input_line_ids.filtered(lambda x: x.amount == 0)
            input_lines.unlink()

    def compute_sheet(self):
        for payslip in self.filtered(lambda slip: slip.state not in ['cancel', 'done']):
            number = payslip.number or self.env['ir.sequence'].next_by_code('salary.slip')
            # delete old payslip lines
            payslip.line_ids.unlink()
            lines = [(0, 0, line) for line in payslip._get_payslip_lines() if line['amount'] != 0]
            payslip.write({'line_ids': lines, 'number': number, 'state': 'verify', 'compute_date': fields.Date.today()})
        return True

    def action_payslip_done(self):
        super(HrPayslip, self).action_payslip_done()
        for rec in self:
            days_lines = rec.worked_days_line_ids.filtered(lambda x: x.number_of_days == 0)
            days_lines.unlink()
            input_lines = rec.input_line_ids.filtered(lambda x: x.amount == 0)
            input_lines.unlink()

    @api.onchange('employee_id', 'struct_id', 'contract_id', 'date_from', 'date_to')
    def _onchange_employee(self):
        self._compute_worked_days_line_ids()
        self._compute_name()
        self.get_inputs()

    def get_inputs_data(self):
        input_values = []
        input_ids = self.struct_id.input_line_type_ids
        utilities_model = self.env['ir.model'].sudo().search([('model', '=', 'data.utilities')])
        if utilities_model:
            utilities_id = self.env['data.utilities'].search([('is_active', '=', True)])
            for input_line in input_ids:
                if input_line.code =='UTL_003':
                    amount = utilities_id.factor_days
                elif input_line.code =='UTL_004':
                    amount = utilities_id.factor_amount
                else:
                    amount = 0
                input_data = {
                    'input_type_id': input_line.id,
                    'code': input_line.code,
                    'name': input_line.name,
                    'contract_id': self.contract_id.id,
                    'amount': amount,
                }
                input_values.append(input_data)
        else:
            # Si el modelo 'data.utilities' no está instalado, establece todos los montos en 0
            for input_line in input_ids:
                input_data = {
                    'input_type_id': input_line.id,
                    'code': input_line.code,
                    'name': input_line.name,
                    'contract_id': self.contract_id.id,
                    'amount': 0,
                }
                input_values.append(input_data)
        return input_values

    def get_inputs(self):
        self.ensure_one()
        input_values = self.get_inputs_data()
        input_lines = self.input_line_ids.browse([])
        for values in input_values:
            input_lines |= input_lines.new(values)
        self.input_line_ids = input_lines