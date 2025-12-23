from odoo.tests import Form
from odoo.addons.hr_contract.tests.common import TestContractCommon
from datetime import date

class TestHrContract(TestContractCommon):

    def setUp(self):
        super().setUp()
        self.employee_regime = self.env['employee.regime'].create({
            'code': '2345',
            'regime_description': 'regime description example',
            'name': 'example name',
            'private_sector': False,             
            'public_sector': True,
            'other_entities': False,
            'is_mype': False
        })
        self.type_contract = self.env['type.contract'].create({
            'code': '2',
            'contract_type': 'contract type description example',
            'name': 'abv'
        })
        self.work_occupation = self.env['work.occupation'].create({
            'code': '1',
            'name': 'worker',
            'executive': False,
            'employee': True,
            'worker': True
        })
        self.contract = self.env['hr.contract'].create({
            'name': 'Contract',
            'employee_id': self.employee.id,
            'state': 'open',
            'kanban_state': 'normal',
            'wage': 1,
            'date_start': date(2023, 1, 1),
            'date_end': date(2023, 1, 31),
            'labor_regime_id': self.employee_regime.id,
            'labor_condition_id': self.type_contract.id,
            'work_occupation_id': self.work_occupation.id,
            'maximum_working_day': True,
            'atypical_cumulative_day': False,
            'nocturnal_schedule': True,
            'unionized': False,
            'is_practitioner': False
        })

    def test_employee_linked_contract(self):
        with Form(self.env['hr.contract']) as form:
            form.name = 'Contract Test'
            form.wage =  1
            form.date_start = date(2024, 1, 1)
            form.date_end =  date(2024, 12, 31)
            form.maximum_working_day = True
            form.atypical_cumulative_day = False
            form.nocturnal_schedule= True
            form.unionized = False
            form.is_practitioner = False
        
        record = form.save()
        self.assertTrue(record, "Formulario no registrado")
        
        self.assertEqual(record.name, 'Contract Test')
        self.assertEqual(record.wage, 1)
        self.assertEqual(record.date_start, date(2024, 1, 1))
        self.assertEqual(record.date_end, date(2024, 12, 31))
        self.assertEqual(record.maximum_working_day, True)
        self.assertEqual(record.atypical_cumulative_day, False)
        self.assertEqual(record.nocturnal_schedule, True)
        self.assertEqual(record.unionized, False)
        self.assertEqual(record.is_practitioner, False)

        print('------TEST ADDITIONAL HR CONTRACT FIELDS OK--------------')

