from datetime import date
from odoo.tests.common import TransactionCase

class TestRatesFifthRent(TransactionCase):

    def setUp(self):
        super().setUp()

        self.uit_data = self.env['various.data.uit'].create({
            'is_active': True,
            'uit_amount': 100.0,
        })
        self.employee = self.env['hr.employee'].create({
            'name': 'Test Employee',
            'active': True,
        })

        self.contract = self.env['hr.contract'].create({
            'name':'Contrato/Empleado',
            'employee_id': self.employee.id,
            'state': 'open',
            'date_start': '2024-01-01',
            'date_end': '2024-12-31',
            'wage':1000,
            'wage_type':'monthly'
        })

        months = [
            ('2024-03-01', '2024-03-31'),
            ('2024-04-01', '2024-04-30'),
            ('2024-05-01', '2024-05-31'),
            ('2024-06-01', '2024-06-30')
        ]
        for date_from, date_to in months:
            payslip = self.env['hr.payslip'].create({
                'name':self.employee.name,
                'employee_id': self.employee.id,
                'date_from': date_from,
                'date_to': date_to,
                'state': 'done'
            })
            self.env['hr.payslip.line'].create({
                'slip_id': payslip.id,
                'code': 'NET',
                'name': 'Net Salary',
                'amount': 1000.00,
                'contract_id': self.contract.id,
                'salary_rule_id':self.env['hr.salary.rule'].search([('code','=','R5T_U01')],limit=1).id
            })

        self.wizard = self.env['payroll.projection.wizard'].create({
            'date_from': '2024-01-01',
            'date_to': '2024-12-31',
            'projection_type': 'current_month',
            'employees_ids': [(6, 0, [self.employee.id])]
        })
    
    def test_calc_rent_5ta(self):
        self.wizard.calc_rent_5ta()

        projection_model = self.env['payroll.projection']
        projection = projection_model.search([
            ('employee_id', '=', self.employee.id),
            ('date_from', '=', '2024-01-01'),
            ('date_to', '=', '2024-12-31')
        ])
        data = projection.line_ids.search([
            ('name','=',self.env.ref('rent_5ta.payroll_projection_exception_total_1').name)
        ])
        self.assertTrue(projection)
        self.assertEqual(projection.state, 'open')
        
        for record in data:
            self.assertEqual(record.may_amount,record.june_amount)
            self.assertEqual(record.may_amount,record.july_amount)

    

    def test_rates_fifth_rent(self):
        rent = self.env['rates.fifth_rent'].create({
            'date_from': '2023-01-01',
            'date_to': '2023-12-31',
        })

        self.assertEqual(rent.date_from, date.fromisoformat('2023-01-01'))
        self.assertEqual(rent.date_to, date.fromisoformat('2023-12-31'))

        rent.write({
            'date_from': '2023-02-01',
            'date_to': '2023-11-30',
        })

        self.assertEqual(rent.date_from, date.fromisoformat('2023-02-01'))
        self.assertEqual(rent.date_to, date.fromisoformat('2023-11-30'))
        print('--------- TEST RATES FIFTH RENT --------------')

    def test_rates_fifth_rent_line(self):
        rent = self.env['rates.fifth_rent'].create({
            'date_from': '2023-01-01',
            'date_to': '2023-12-31',
        })

        rent_line = self.env['rates.fifth_rent.line'].create({
            'sequence': 1,
            'rate_parent_id': rent.id,
            'name': 'Tramo 1',
            'value_from': 0,
            'value_to': 1000,
            'percent': 10.0,
        })

        self.assertEqual(rent_line.sequence, 1)
        self.assertEqual(rent_line.name, 'Tramo 1')
        self.assertEqual(rent_line.value_from, 0)
        self.assertEqual(rent_line.value_to, 1000)
        self.assertEqual(rent_line.percent, 10.0)

        rent_line.write({
            'name': 'Tramo 2',
            'percent': 15.0,
        })

        self.assertEqual(rent_line.name, 'Tramo 2')
        self.assertEqual(rent_line.percent, 15.0)

        updated_values = rent_line.set_amount_per_record({
            'value_from': 500,
            'value_to': 800,
        })
        print('--------- TEST RATES FIFTH RENT LINE --------------')