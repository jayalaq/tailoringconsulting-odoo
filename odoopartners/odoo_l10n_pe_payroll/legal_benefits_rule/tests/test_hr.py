from datetime import *
from odoo.tests.common import TransactionCase


class TestHr(TransactionCase):

    def setUp(self, *args, **kwargs):
        super(TestHr, self).setUp(*args, **kwargs)
        self.employee = self.env['hr.employee'].create({
            'name': 'Test Employee',
            'service_hire_date': date.today()
        })
        self.calendar = self.env['resource.calendar'].create({
            'name': 'Test Calendar',
            'hours_per_day': 8.0, 
        })
        self.contract = self.env['hr.contract'].create({
            'name': 'Test Contract',
            'employee_id': self.employee.id,
            'resource_calendar_id': self.calendar.id,
            'date_start': datetime.now().strftime('%Y-%m-%d'),
            'wage': 0.0, 
        })
        self.payslip = self.env['hr.payslip'].create({
            'name': 'Test Payslip',
            'employee_id': self.employee.id,
            'date_from': datetime.now().strftime('%Y-01-01'),
            'date_to': datetime.now().strftime('%Y-01-31'),
            'contract_id': self.contract.id,
        })

    def test_get_worked_day_lines(self):
        payslip = self.payslip
        
        tdi_001_entry_type_id = self.env.ref('legal_benefits_rule.hr_work_entry_type_tdi_001')
        tdi_002_entry_type_id = self.env.ref('legal_benefits_rule.hr_work_entry_type_tdi_002')
        
        hours_per_day = payslip.contract_id.resource_calendar_id.hours_per_day or 0.0
        date_start, year, month, _ = payslip.generate_date_start_month_year(payslip.date_from, payslip.date_to)
        month = int(month)
        year = int(year)
        start_m, star_y = payslip._get_month(year, month, 6)
        end_m, end_y = payslip._get_month(year, month, 1)
        periods = payslip._get_periods(start_m, star_y, end_m, end_y)
        service_date = '{}/{}'.format(payslip.employee_id.service_hire_date.strftime('%m'), payslip.employee_id.service_hire_date.strftime('%Y'))
        worked_lines = self.env['hr.payslip.worked_days'].search([
                    ('date_start', 'in', periods),
                    ('employee_id', '=', payslip.employee_id.id),
                    ('number_of_days', '>', 0)
        ])
    
        self.payslip.write({
            'worked_days_line_ids': [
                    (0, 0, {'code': 'TDI_001', 'number_of_days': 5, 'work_entry_type_id': tdi_001_entry_type_id.id}),
                    (0, 0, {'code': 'TDI_002', 'number_of_days': 10, 'work_entry_type_id': tdi_002_entry_type_id.id}),
                ]
        })

        # Llama al método _get_worked_day_lines para realizar el cálculo
        self.payslip._get_worked_day_lines()

        # Verifica los resultados esperados
        tdi_001_days = self.payslip.worked_days_line_ids.filtered(lambda line: line.code == 'TDI_001').number_of_days
        tdi_002_days = self.payslip.worked_days_line_ids.filtered(lambda line: line.code == 'TDI_002').number_of_days

        self.assertEqual(tdi_001_days, 5, 'testito1')
        self.assertEqual(tdi_002_days, 10, 'testito2')
        self.assertFalse(payslip.get_calc_tdi_days(worked_lines,periods,'TDI_002'))
        self.assertFalse(payslip.get_calc_tdl_days(worked_lines,periods,'TDL_002'))
        self.assertFalse(payslip._get_calc_dias_003(worked_lines, payslip.employee_id, date_start))
        self.assertFalse(payslip._get_calc_cts_grat_per_days( periods, payslip.contract_id, date_start, month, 'CTS_002'))
