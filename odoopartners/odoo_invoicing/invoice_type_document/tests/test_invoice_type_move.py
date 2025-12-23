from odoo.tests.common import TransactionCase
from odoo.tests import tagged
from odoo.exceptions import ValidationError
from odoo import fields, Command


@tagged('post_install', '-at_install')
class TestInvoiceTypeMove(TransactionCase):
    
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.company = cls.env['res.company'].search([])
        cls.account = cls.env['account.account'].search([
                    ('company_id', '=', cls.company[0].id),
                    ('account_type', '=', 'income'),
                ], limit=1),
     
        cls.move = cls.env['account.move'].create({
            'name': 'Factura TEST',
            'date': fields.Date.from_string('2024-06-04'),
            'serie_correlative':'E003-03',
            'move_type': 'entry',
        })
        
    def setUp(self):
        super(TestInvoiceTypeMove, self).setUp()
        
        self.ts_account_move_line = self.env['account.move.line'].create({
            'move_id': self.move.id,
            'name': 'product 1',
            'account_id': 3,  
            'debit': 0.00,  
            'credit': 0.00,
            'move_type': 'entry',
            'serie_correlative':'E003-03',
            'serie_correlative_is_readonly': False
        })
          
        print("----SETUP OK----")
                
    def test_fields_invoice_account_move(self):
        self.assertEqual(self.ts_account_move_line.move_id.id,self.move.id)
        self.assertEqual(self.ts_account_move_line.name,'product 1')
        self.assertEqual(self.ts_account_move_line.account_id.id, 3)
        self.assertEqual(self.ts_account_move_line.debit, 0.00)
        self.assertEqual(self.ts_account_move_line.credit, 0.00)
        self.assertEqual(self.ts_account_move_line.move_type, 'entry')
        self.assertFalse(self.ts_account_move_line.serie_correlative_is_readonly)
        self.assertEqual(self.move.serie_correlative, 'E003-03')
        print("-------TEST FIELDS INVOICE OK-----")
    
    def test_function_invoice_move(self):
        latam_type = self.env['l10n_latam.document.type'].search([],limit=1)
        vals_list = [{
            'sequence': 100,
            'product_id': 1,
            'name': 'Product Classic',
            'account_id': 1106,
            'analytic_distribution': False,
            'deferred_start_date': False,
            'deferred_end_date': False,
            'quantity': 1,
            'product_uom_id': 1,
            'price_unit': 100,
            'discount': 0,
            'l10n_pe_is_detraction_retention': False,
            'l10n_pe_edi_allowance_charge_reason_code': False,
            'tax_ids': [[4, 16]],
            'l10n_pe_edi_affectation_reason': '10',
            'partner_id': 7,
            'currency_id': 155,
            'purchase_line_id': False,
            'display_type': 'product',
            'subscription_id': False,
            'move_id': 251,
            'l10n_latam_document_type_id':latam_type.id
            }]
        
        res_create = self.ts_account_move_line.create(vals_list)
        self.move.action_post()
        
        self.assertTrue(res_create)
        self.assertIsNone(self.ts_account_move_line._compute_serie_correlative_is_readonly())