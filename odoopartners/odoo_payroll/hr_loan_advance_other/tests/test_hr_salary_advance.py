import logging

from odoo.tests import tagged
from odoo.addons.hr_payroll.tests.common import TestPayslipBase
from odoo.fields import Date
from dateutil.relativedelta import relativedelta

_logger = logging.getLogger(__name__)


@tagged('-at_install', 'post_install')
class TestHrSalaryAdvance(TestPayslipBase):

    @classmethod
    def setUpClass(cls):
        super(TestHrSalaryAdvance, cls).setUpClass()
        cls.richard_emp.private_street = "Calle Ejemplo"
        cls.structure_type.default_struct_id.max_percent = 1
        cls.structure_type.default_struct_id.advance_date = 1

    def create_advance_salary(cls):
        
        contract = cls.env['hr.contract'].create({
            'date_end': Date.today() + relativedelta(years=2),
            'date_start': Date.to_date('2018-01-01'),
            'name': 'Contract for Richard',
            'wage': 5000.33,
            'employee_id': cls.richard_emp.id,
            'structure_type_id': cls.structure_type.id,
        })
        return cls.env['hr.salary.advance'].create({
            'advance': 1.0,
            'employee_id': cls.richard_emp.id,
            'employee_contract_id': contract.id,
        })
    
    def test_approve_salary_advance(cls):
        advance_salary = cls.create_advance_salary()
        advance_salary.approve_request()
        cls.assertEqual(
            advance_salary.state, 'waiting_approval',
            'The advance salary must be in final stage to approve it.',
        )
        _logger.info('Test approve request advance salary passed')
    
    def test_compute_sheet(cls):
        specific_structure = cls.env.ref('hr_loan_advance_other.hr_payroll_structure_loans')

        payslip_run = cls.env['hr.payslip.run'].create({
            'date_end': '2024-07-01',
            'date_start': '2022-09-01',
            'name': 'Payslip for Employee'
        })

        payslip_employee = cls.env['hr.payslip.employees'].create({
            'employee_ids': [(4, cls.richard_emp.id)],
            'structure_id': specific_structure.id,
        })

        payslip_employee.with_context(active_id=payslip_run.id).compute_sheet()
        _logger.info('Test compute sheet')