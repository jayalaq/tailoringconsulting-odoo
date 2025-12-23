from odoo.tests.common import TransactionCase
from datetime import date


class TestHrPayslipDias010(TransactionCase):

    def setUp(self):
        super().setUp()
        self.company = self.env['res.company'].create({
            'name': 'Test Company',
        })
        self.employee = self.env['hr.employee'].create({
            'name': 'Test Employee',
            'company_id': self.company.id,
        })
        self.contract = self.env['hr.contract'].create({
            'name': 'Test Contract',
            'employee_id': self.employee.id,
            'wage': 1000.0,
            'state': 'open',
            'date_start': date(2022, 1, 1),
            'resource_calendar_id': self.env['resource.calendar'].create({
                'name': 'Test Calendar',
                'hours_per_day': 8,
            }).id,
        })

        self.struct = self.env.ref('rules_utilities.hr_payroll_structure_utilidades')
        self.payslip = self.env['hr.payslip'].create({
            'name': 'Test Payslip',
            'employee_id': self.employee.id,
            'contract_id': self.contract.id,
            'date_from': date(2023, 7, 1),
            'date_to': date(2023, 7, 31),
            'struct_id': self.struct.id,
        })

    def test_get_worked_day_lines_with_utilidades_structure(self):
        work_entry_type = self.env['hr.work.entry.type'].search([('code', '=', 'WORK100')], limit=1)
        if not work_entry_type:
            work_entry_type = self.env['hr.work.entry.type'].create({
                'name': 'Regular Working Day',
                'code': 'WORK100',
                'utilities': True,
            })

        previous_year = self.payslip.date_to.year - 1
        self.env['hr.payslip.worked_days'].create({
            'date_from': date(previous_year, 1, 1),
            'date_to': date(previous_year, 12, 31),
            'employee_id': self.employee.id,
            'number_of_days': 240,
            'work_entry_type_id': work_entry_type.id,
            'payslip_id': self.payslip.id, 
        })

        result = self.payslip._get_worked_day_lines()
        dias_010_type = self.env.ref('rules_utilities.hr_work_entry_type_dias_010')

        # Verificar que DIAS_010 está incluido en el resultado
        dias_010_line = next((line for line in result if line['work_entry_type_id'] == dias_010_type.id), None)
        self.assertIsNotNone(dias_010_line, "Línea de DIAS_010 no encontrada en las líneas de días trabajados")
        print('------------------------TEST OK---------------------------')
