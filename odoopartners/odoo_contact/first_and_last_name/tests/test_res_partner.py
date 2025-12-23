from odoo.tests.common import TransactionCase


class TestResPartner(TransactionCase):
     def setUp(self):
        super(TestResPartner, self).setUp()
        self.partner = self.env['res.partner'].create({
            'name': 'John Doe',
            'partner_name': 'John',
            'first_name': 'Doe',
            'second_name': 'Smith'
        })

    def test_partner_fields(self):
        self.assertEqual(self.partner.name, 'John Doe Smith', "Partner's full name should be John Doe Smith")
        self.assertEqual(self.partner.partner_name, 'John', "Partner's name should be John")
        self.assertEqual(self.partner.first_name, 'Doe', "Partner's first name should be Doe")
        self.assertEqual(self.partner.second_name, 'Smith', "Partner's last name should be Smith")
        print('------------------ FULL NAME TEST --------------------')