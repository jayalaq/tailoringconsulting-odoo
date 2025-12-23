from odoo import fields
from odoo.tests import common
from dateutil.relativedelta import relativedelta

@common.tagged('post_install', '-at_install')
class TestEmployeeServiceContract(common.TransactionCase):

    def setUp(self):
        super().setUp()

        self.today = fields.Date.today()
        self.now = fields.Datetime.now()
        self.Employee = self.env['hr.employee']
        self.SudoEmployee = self.Employee.sudo()
        self.Contract = self.env['hr.contract']
        self.SudoContract = self.Contract.sudo()

    def test_employee_contract_1(self):
        employee = self.SudoEmployee.create({
            'name': 'Employee #1',
            'contract_ids': [
                (0, 0, {
                    'name': 'Employee #1 Contract #1',
                    'wage': 5000.0,
                    'state': 'close',
                    'date_start': self.today - relativedelta(years=3),
                    'date_end': self.today - relativedelta(years=1),
                }),
            ],
        })

        self.assertEqual(
            employee.service_start_date,
            self.today - relativedelta(years=3)
        )
        self.assertEqual(
            employee.service_termination_date,
            self.today - relativedelta(years=1)
        )

    def test_employee_contract_2(self):
        employee = self.SudoEmployee.create({
            'name': 'Employee #2',
            'contract_ids': [
                (0, 0, {
                    'name': 'Employee #2 Contract #1',
                    'wage': 5000.0,
                    'state': 'open',
                    'date_start': self.today - relativedelta(years=3),
                }),
            ],
        })

        self.assertEqual(employee.service_start_date,self.today - relativedelta(years=3))
        self.assertEqual(employee.service_termination_date,False)

    def test_employee_contract_3(self):
        employee = self.SudoEmployee.create({
            'name': 'Employee #3',
            'contract_ids': [
                (0, 0, {
                    'name': 'Employee #3 Contract #1',
                    'wage': 5000.0,
                    'state': 'close',
                    'date_start': self.today - relativedelta(years=5),
                    'date_end': self.today - relativedelta(years=1),
                })
            ]
        })

        self.assertEqual(employee.service_start_date,self.today - relativedelta(years=5))

    def test_employee_contract_4(self):
        employee = self.SudoEmployee.create({
            'name': 'Employee #4',
            'contract_ids': [
                (0, 0, {
                    'name': 'Employee #4 Contract #1',
                    'wage': 5000.0,
                    'state': 'close',
                    'date_start': self.today - relativedelta(years=5),
                    'date_end': self.today - relativedelta(years=1)
                })
            ]
        })

        self.assertEqual(employee.service_start_date,self.today - relativedelta(years=5))
        self.assertEqual(employee.service_termination_date,self.today - relativedelta(years=1))

