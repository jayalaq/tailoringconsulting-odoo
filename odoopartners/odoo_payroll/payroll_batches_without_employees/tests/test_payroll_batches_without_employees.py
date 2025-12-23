from odoo.tests.common import TransactionCase

class TestPayrollBatchesWithoutEmployees(TransactionCase):

    def setUp(self):
        super(TestPayrollBatchesWithoutEmployees, self).setUp()
        # Creación de un empleado de prueba
        self.employee = self.env['hr.employee'].create({
            'name': 'Test Employee',
        })
        # Creación del wizard hr.payslip.employees
        self.payslip_employees_wizard = self.env['hr.payslip.employees'].create({
            'employee_ids': [(4, self.employee.id)]
        })

    def test_clean_employees_button(self):
        # Verificar que el empleado está inicialmente en la lista
        self.assertEqual(len(self.payslip_employees_wizard.employee_ids), 1, "Initially, the employee list should have one employee")

        # Llamar al método clean_employees
        self.payslip_employees_wizard.clean_employees()

        # Verificar que la lista de empleados está vacía después de llamar al método
        self.assertEqual(len(self.payslip_employees_wizard.employee_ids), 0, "The employee list should be empty after cleaning")

        print('-------TEST PAYROLL BATCHES WITHOUT EMPLOYEES OK ----------------')
