from odoo.tests.common import TransactionCase
from odoo.exceptions import ValidationError


class TestJudicialRetentionFields(TransactionCase):

    def setUp(self):
        super(TestJudicialRetentionFields, self).setUp()
        self.hr_employee = self.env['hr.employee']
        self.hr_contract = self.env['hr.contract']
        self.hr_payslip = self.env['hr.payslip']

    def test_01_create_employee(self):
        try:
            self.employee = self.hr_employee.create({
                'name': 'Fernando Pastor',
            })
        except Exception as e:
            self.fail(f"Creation of employee failed: {e}")

    def test_02_create_judicial_retention(self):
        self.test_01_create_employee()
        contract = self.hr_contract.create({
            'name': 'Contract for Fernando Pastor',
            'employee_id': self.employee.id,
            'wage': 1000,
            'state': 'draft',
        })
        contract.write({'state': 'open'})

        payslip = self.hr_payslip.create({
            'name': 'Payslip for Fernando Pastor',
            'employee_id': self.employee.id,
            'contract_id': contract.id,
            'date_from': '2024-06-01',
            'date_to': '2024-06-30',
        })

        try:
            payslip.action_get_judicial_format()
        except ValidationError as e:
            self.fail(f"Report generation failed: {e}")
        except Exception as e:
            if "unexpected error" in str(e).lower():
                self.fail(f"Test failed due to unexpected error message: {e}")
