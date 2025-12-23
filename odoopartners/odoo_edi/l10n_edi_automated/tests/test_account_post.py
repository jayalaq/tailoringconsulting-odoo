from odoo.addons.account.tests.common import AccountTestInvoicingCommon
from odoo.tests import tagged
from odoo.tests.common import Form
from odoo.exceptions import UserError, ValidationError
from odoo.tools import mute_logger
import psycopg2


@tagged('post_install', '-at_install')
class TestAccountAccount(AccountTestInvoicingCommon):

    def test_changing_account_company(self):
        ''' Ensure you can't change the company of an account.account if there are some journal entries '''

        self.env['account.move'].create({
            'move_type': 'entry',
            'date': '2019-01-01',
            'line_ids': [
                (0, 0, {
                    'name': 'line_debit',
                    'account_id': self.company_data['default_account_revenue'].id,
                }),
                (0, 0, {
                    'name': 'line_credit',
                    'account_id': self.company_data['default_account_revenue'].id,
                }),
            ],
        })

        with self.assertRaises(UserError), self.cr.savepoint():
            self.company_data['default_account_revenue'].company_id = self.company_data_2['company']

    def test_toggle_reconcile(self):
        ''' Test the feature when the user sets an account as reconcile/not reconcile with existing journal entries. '''
        account = self.company_data['default_account_revenue']

        move = self.env['account.move'].create({
            'move_type': 'entry',
            'date': '2019-01-01',
            'line_ids': [
                (0, 0, {
                    'account_id': account.id,
                    'currency_id': self.currency_data['currency'].id,
                    'debit': 100.0,
                    'credit': 0.0,
                    'amount_currency': 200.0,
                }),
                (0, 0, {
                    'account_id': account.id,
                    'currency_id': self.currency_data['currency'].id,
                    'debit': 0.0,
                    'credit': 100.0,
                    'amount_currency': -200.0,
                }),
            ],
        })
        move.action_post()
        self.env['account.move.line'].flush_model()

        self.assertRecordValues(move.line_ids, [
            {'reconciled': False, 'amount_residual': 0.0, 'amount_residual_currency': 0.0},
            {'reconciled': False, 'amount_residual': 0.0, 'amount_residual_currency': 0.0},
        ])

        # Set the account as reconcile and fully reconcile something.
        account.reconcile = True
        self.env.invalidate_all()

        self.assertRecordValues(move.line_ids, [
            {'reconciled': False, 'amount_residual': 100.0, 'amount_residual_currency': 200.0},
            {'reconciled': False, 'amount_residual': -100.0, 'amount_residual_currency': -200.0},
        ])

        move.line_ids.reconcile()
        self.assertRecordValues(move.line_ids, [
            {'reconciled': True, 'amount_residual': 0.0, 'amount_residual_currency': 0.0},
            {'reconciled': True, 'amount_residual': 0.0, 'amount_residual_currency': 0.0},
        ])

        # Set back to a not reconcile account and check the journal items.
        move.line_ids.remove_move_reconcile()
        account.reconcile = False
        self.env.invalidate_all()

        self.assertRecordValues(move.line_ids, [
            {'reconciled': False, 'amount_residual': 0.0, 'amount_residual_currency': 0.0},
            {'reconciled': False, 'amount_residual': 0.0, 'amount_residual_currency': 0.0},
        ])
        print('TEST OK ACTION POST-------------------------')
