from odoo import fields
from odoo.tests import common

@common.tagged('post_install', '-at_install')
class TestAccountMove(common.TransactionCase):

    def setUp(self):
        super().setUp()
        self.partner_id_address_origin=self.env['res.partner'].create({
            'name': 'Test Move Line address origin',
        })
        self.partner_id_address_destiny=self.env['res.partner'].create({
            'name': 'Test Move Line address destiny',
        })
        self.account_move_line = self.env['account.move.line'].create({
            'name': 'Test Move',
            'origin_address': self.partner_id_address_origin.id,
            'destiny_address': self.partner_id_address_destiny.id,
        })

    def test_aditional_document_reference_field(self):
        self.assertTrue(hasattr(self.account_move_line, 'origin_address'))
        self.assertTrue(hasattr(self.account_move_line, 'destiny_address'))

        self.assertIsInstance(self.account_move_line.origin_address.name, str)
        self.assertIsInstance(self.account_move_line.destiny_address.name, str)

        self.assertEqual(self.account_move_line.origin_address.name, 'Test Move Line address origin')
        self.assertEqual(self.account_move_line.destiny_address.name, 'Test Move Line address destiny')