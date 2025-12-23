
from odoo.exceptions import ValidationError
from odoo.tests.common import TransactionCase


class TestCompany(TransactionCase):

    def test_check_active(self):
        """
        Tests the ability to archive a company whether or not it still has active users.
        """
        self.partner_demo = self.env['res.partner'].create({
            'name': 'Marc Demo',
            'email': 'mark.brown23@example.com',
        })
        self.company = self.env['res.company'].create({
            'name': 'foo',
            'legal_representative': self.partner_demo.id,
            'object_company': 'Texto de prueba',
        })

        self.user = self.env['res.users'].create({
            'name': 'foo',
            'login': 'foo',
            'company_id': self.company.id,
            'company_ids': self.company.ids,
            'notification_type':'email',
        })  
            
        # La empresa no se puede archivar porque aún tiene usuarios activos
        with self.assertRaisesRegex(ValidationError, 'La empresa foo no se puede archivar porque todavía se utiliza como la empresa predeterminada de los usuarios'):
            self.company.action_archive()


        # The company can be archived because it has no active users
        self.user.action_archive()
        self.company.action_archive()

        # The user can be unarchived once we set another, active, company
        self.main_company = self.env.ref('base.main_company')
        self.user.write({
            'company_id': self.main_company.id,
            'company_ids': self.main_company.ids,
        })
        self.user.action_unarchive()
        print('-------------TEST LEGAL DATA OK-------------')
