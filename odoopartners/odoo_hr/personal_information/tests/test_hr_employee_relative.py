from datetime import datetime

from dateutil.relativedelta import relativedelta
from odoo.tests import Form, common


@common.tagged('post_install', '-at_install')
class TestHrEmployeeRelatives(common.TransactionCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.relation_sibling = cls.env.ref('personal_information.relation_sibling')
        cls.partner_1 = cls.env['res.partner'].create({'name': 'Marco Vasquez'})
        cls.partner_2 = cls.env['res.partner'].create({'name': 'Arturo Jesus'})

    def setUp(self):
        super().setUp()
        self.employee = self.env['hr.employee'].create({
            'name': 'Leo Daniel Flores Sánchez',
            'relative_ids': [(0, 0, {
                'relation_id': self.relation_sibling.id,
                'partner_id': self.partner_1.id,
                'name': 'Marco Vasquez',
                'gender': 'masculino',
                'phone_number': '+51 982367182',
                'job': 'Ingeniero de Software',
                'notes': 'Esta es una nota :D',
                'date_of_birth': datetime.now() - relativedelta(years=28),
            })]
        })
        self.employee_relative = self.env['hr.employee.relative'].browse(self.employee.relative_ids[0].id)

    def test_age_calculation(self):
        """Test age calculation for employee relatives."""
        self.assertEqual(self.employee_relative.age, 28)

        new_date_of_birth = datetime.now() - relativedelta(years=45)
        self.employee_relative.write({'date_of_birth': new_date_of_birth})
        self.assertEqual(self.employee_relative.age, 45)

    def test_onchange_employee_relative_name(self):
        """Test onchange method for relative name."""
        self.assertEqual(self.employee_relative.name, 'Marco Vasquez')

        with Form(self.employee_relative) as f:
            f.partner_id = self.partner_2
        self.assertEqual(
            self.employee_relative.name, 
            self.employee_relative.partner_id.display_name
        )

    def test_write_employee_name_lastname(self):
        """Test writing employee name, last name and second last name."""
        self.employee.write({
            'firstname': 'Leo Daniel',
            'lastname': 'Flores',
            'secondname': 'Sánchez'
        })
        self.assertEqual(self.employee.firstname, 'Leo Daniel')
        self.assertEqual(self.employee.lastname, 'Flores')
        self.assertEqual(self.employee.secondname, 'Sánchez')
