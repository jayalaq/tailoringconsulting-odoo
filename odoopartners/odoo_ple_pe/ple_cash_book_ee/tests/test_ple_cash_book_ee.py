from pytz import timezone
from datetime import *

from odoo.tests.common import tagged
from odoo.tests import common

@tagged('post_install', '-at_install')
class TestPleCashBookee(common.TransactionCase):

    def setUp(self):
        super().setUp()
        
        self.company_data = self.env['res.company'].create({
            'name':'Company Peruvian',
            'vat': "20557912879",
            'country_id': self.env.ref('base.pe').id,
            'ple_type_contributor': 'CUO',
        })
          
        self.partner_a = self.env['res.partner'].create({
            'name':'Comperuvian',
            'vat': '20462509236',
            'l10n_latam_identification_type_id': self.env.ref('l10n_pe.it_RUC').id,
            'country_id': self.env.ref('base.pe').id,
        })  
        
        self.tax_group = self.env['account.tax.group'].create({
            'name': "IGV",
            'l10n_pe_edi_code': "IGV",
        })

        self.tax_18 = self.env['account.tax'].create({
            'name': 'tax_18',
            'amount_type': 'percent',
            'amount': 18,
            'l10n_pe_edi_tax_code': '1000',
            'l10n_pe_edi_unece_category': 'S',
            'type_tax_use': 'sale',
            'tax_group_id': self.tax_group.id,
        })  
            
        self.product = self.env['product.product'].create({
            'name': 'product_ple',
            'uom_po_id': self.env.ref('uom.product_uom_kgm').id,
            'uom_id': self.env.ref('uom.product_uom_kgm').id,
            'lst_price': 1000.0,
        })
        
        self.account_cash = self.env['account.account'].search([('code','=','1010000')],limit=1)
        self.account_bank = self.env['account.account'].search([('code','=','1041001')],limit=1)
        
        self.currency_data = self.env['res.currency'].search([('name','=','PEN')])
        
    def test_ple_invoice(self):
        self.account_cash.write({'ple_selection':'cash'})
        self.account_bank.write({'ple_selection':'bank'})

        account_move = self.env['account.move'].create({
            'name': 'Factura Contable',
            'move_type': 'in_invoice',
            'partner_id': self.partner_a.id,
            'invoice_date': '2023-11-29',
            'date': '2023-1-29',
            'currency_id': self.currency_data.id,
            'exchange_rate': 1.000000,
            'invoice_line_ids': [
                (0, 0, {
                    'account_id':self.account_cash.id,
                    'ple_correlative':'M000000001',
                    'partner_id':self.partner_a.id,
                    'l10n_latam_document_type_id': self.env.ref('l10n_pe.document_type01').id,
                    'debit':100,
                    'credit':0,
                }),
                (0, 0, {
                    'account_id':self.account_bank.id,
                    'ple_correlative':'M000000002',
                    'partner_id':self.partner_a.id,
                    'l10n_latam_document_type_id': self.env.ref('l10n_pe.document_type01').id,
                    'debit':0,
                    'credit':100,
                })
            ]
        })
        account_move.action_post()
        self.assertTrue(account_move)
        
    def test_report_cash_bank(self):
        ple_cash_bank = self.env['ple.report.cash.bank'].create({
            'company_id':self.company_data.id,
            'date_start':'2023-01-01',
            'date_end':'2023-12-31',
            'state_send':'1'
        })
        
        ple_cash_bank.action_generate_excel()
        self.assertEqual(ple_cash_bank.date_ple,date.today())

        self.assertTrue(ple_cash_bank.xls_filename_cash)
        self.assertTrue(ple_cash_bank.txt_filename_cash)

        self.assertTrue(ple_cash_bank.xls_filename_bank)
        self.assertTrue(ple_cash_bank.txt_filename_bank)

        

