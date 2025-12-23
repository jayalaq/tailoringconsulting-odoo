from odoo.addons.account.tests.common import AccountTestInvoicingCommon
from odoo.exceptions import AccessError
from odoo.tests import tagged


@tagged('post_install', '-at_install')
class TestMassivePaymentCollections(AccountTestInvoicingCommon):
    def test_massive_payment_collection(self):
        self = self.env['account.move.line']
        lines_model = self.env['account.move.line'].browse(self._context.get('active_ids', []))
        available_lines = self.env['account.move.line'].search([])
        valid_account_types = self.env['account.payment']._get_valid_payment_account_types()
        for line in lines_model:
            self.assertTrue(line in available_lines)
            self.assertNotIn(line.move_id.state, ['posted'])
            self.assertNotIn(line.account_type, valid_account_types)
            self.assertRaises(AccessError, line.__create_payments())
        print('-------------TEST MASSIVE_PAYMENT_COLLECTIONS OK-------------')