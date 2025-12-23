from odoo import fields
from odoo.tests import common

@common.tagged('post_install', '-at_install')
class TestAccountMove(common.TransactionCase):

    def setUp(self):
        super().setUp()
        self.account_move = self.env['account.move'].create({
            'name': 'Test Move',
            'aditional_document_reference': 'Test Document Reference'
        })

    def test_aditional_document_reference_field(self):
        self.assertTrue(hasattr(self.account_move, 'aditional_document_reference'))

        self.assertIsInstance(self.account_move.aditional_document_reference, str)

        self.assertEqual(self.account_move.aditional_document_reference, 'Test Document Reference')