from odoo.tests import tagged
from odoo.tests.common import TransactionCase

@tagged('-at_install', 'post_install')
class TestCompensatedHours(TransactionCase):

    @classmethod
    def setUpClass(cls):
        super(TestCompensatedHours, cls).setUpClass()
        cls.employee = cls.env['hr.employee'].create({
            'name': 'Empleado de Prueba',
        })
        cls.account_analytic_line = cls.env['account.analytic.line'].create({
            'name': 'Test Line',
            'employee_id': cls.employee.id,
            'unit_amount': 4,
            'hours_compensate': 4,
            'is_validate_extra_hour': False,
        })
        cls.holiday_status_id = cls.env.ref('automatic_leave_type.hr_leave_type_27', False)


    def test_action_validate_extra_hours(self):
        self.account_analytic_line.action_validate_extra_hours()
        self.assertTrue(self.account_analytic_line.is_validate_extra_hour, "La línea no se marcó como validada después de ejecutar la acción.")
        print('------------TEST OK----------------------')