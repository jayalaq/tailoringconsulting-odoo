from odoo.addons.base.tests.common import SavepointCaseWithUserDemo

class TestCarrierRefNumInvoice(SavepointCaseWithUserDemo):
    """Tests carrier_ref_number
    """
    def test_set_carrier_ref_number(self):
        account_move_model = self.env['account.move']
        carrier_ref_number = "123456789"
        currency_id = self.env['res.currency'].search([])[0].id
        journal_id = self.env['account.journal'].search([])[0].id
        account_move_unit = account_move_model.create({
            'journal_id': journal_id,
            'currency_id': currency_id,
            'carrier_ref_number': carrier_ref_number,
            'auto_post': 'no',
            'date': '2020-01-01',
            'extract_state': 'no_extract_requested',
            'move_type': 'out_invoice',
            'state': 'draft'
        })
        vals = account_move_model.search([('carrier_ref_number', '=', carrier_ref_number)])
        self.assertEqual(1, len(vals))
        self.assertEqual(account_move_unit, vals[0])
        vals = account_move_model.search([('carrier_ref_number', 'in', [carrier_ref_number])])
        self.assertEqual(1, len(vals))
        self.assertEqual(account_move_unit, vals[0])
        self.assertEqual(vals[0].carrier_ref_number, carrier_ref_number)

        print('-------------TEST CARRIER_REF_NUM_INVOICE OK-------------')