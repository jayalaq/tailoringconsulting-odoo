from odoo.tests import tagged
from odoo.tests import Form
from odoo.addons.hr_contract.tests.common import TestContractCommon
from datetime import date

@tagged('-at_install', 'post_install')
class TestHrContract(TestContractCommon):

    def setUp(self):
        super().setUp()
        self.low_reason = self.env['low.reason'].create({
            'code': '2',
            'low_reason_description': 'low reason description example',
            'name': 'abv'
        })
        self.mintra_contract = self.env['mintra.contract'].create({
            'code': '1',
            'mintra_description': 'mintra  contract description example'
        })
        self.payment_period = self.env['payment.period'].create({
            'code': 'codigo prueba',
            'payment_description': 'descripcion prueba',
            'name': 'nombre prueba'
        })
        self.specific_structure = self.env['hr.payroll.structure'].create({
            'name': 'End of the Year Bonus - Test',
            'schedule_pay_conditions': self.payment_period.id,
            'type_id': 1,
        })
        self.structure_type = self.env['hr.payroll.structure.type'].create({
            'name': 'struct',
            'default_struct_id': self.specific_structure.id
        })
        self.contract = self.env['hr.contract'].create({
            'name': 'Contract',
            'employee_id': self.employee.id,
            'state': 'open',
            'kanban_state': 'normal',
            'wage': 1,
            'date_start': date(2024, 2, 1),
            'date_end': date(2024, 2, 29),
            'reason_low_id': self.low_reason.id,
            'mintra_contract_id': self.mintra_contract.id,
            'compensation_in_kind': False,
            'structure_type_id': self.structure_type.id
        })

    def test_employee_linked_contract(self):
        value = self.specific_structure.get_additional_certificate_name()
        self.assertEqual(self.employee.contract_id, self.contract)
        print('------TEST ADDITIONAL PAYROLL FIELDS OK--------------')