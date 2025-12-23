from odoo.tests.common import TransactionCase
from odoo.tests import tagged
from datetime import *

@tagged('post_install', '-at_install')
class TestPleInvBal03(TransactionCase):

    def setUp(self):
        super().setUp()
            
        self.ple_report = self.env['ple.report.inv.bal.03'].create({
            'date_start': date(2024,1,1),
            'date_end': date(2024,12,31),
            'financial_statements_catalog': '07',
            'eeff_presentation_opportunity': '01',
            'state_send': '1' 
        })
        self.ple_inv_one = self.env['ple.report.inv.bal.one'].create({
            'company_id':self.env.company.id,
            'date_start': date(2024,1,1),
            'date_end': date(2024,12,31),
            'state_send': '1', 
            'eeff_presentation_opportunity': '01'
        })
        
        self.product = self.env['product.product'].create({
            'name': 'producto test',
            'uom_po_id': self.env.ref('uom.product_uom_kgm').id,
            'uom_id': self.env.ref('uom.product_uom_kgm').id,
            'lst_price': 1000.0,
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
        
        self.customer_invoice = self.env['account.move'].create({
            'name':'Factura cliente',
            'invoice_date':date.today(),
            'journal_id':self.env['account.journal'].search([('type','=','sale')],limit=1).id,
            'currency_id': self.env['res.currency'].search([('name','=','PEN')]).id,
            'l10n_latam_document_type_id': self.env.ref('l10n_pe.document_type01').id,
            'invoice_line_ids': [(0, 0, {
                'product_id': self.product.id,
                'product_uom_id': self.env.ref('uom.product_uom_kgm').id,
                'price_unit': 2000.0,
                'quantity': 5,
                'tax_ids': [(6, 0, self.tax_18.ids)],
            })],
        })
    
    def test_action_generate_report(self):
        self.ple_report.action_generate_report()
        self.assertEqual(self.ple_report.date_start, date(2024, 1, 1))
        self.assertEqual(self.ple_report.date_end, date(2024, 12, 31))
        self.assertEqual(self.ple_report.financial_statements_catalog,'07')
        self.assertEqual(self.ple_report.eeff_presentation_opportunity,'01')
        self.assertEqual(self.ple_report.state_send,'1')
        
        self.assertTrue(self.ple_report.exists())

    def test_action_generate_excel(self):
        self.ple_report.action_generate_excel()
        
        self.assertTrue(self.ple_report.xls_filename)
        self.assertTrue(self.ple_report.xls_binary)

    def test_action_ple_inv_one_generate_excel(self):
        self.ple_inv_one.action_generate_excel()

        self.assertEqual(self.ple_inv_one.date_start, date(2024, 1, 1))
        self.assertEqual(self.ple_inv_one.date_end, date(2024, 12, 31))
        self.assertEqual(self.ple_inv_one.eeff_presentation_opportunity,'01')
        self.assertEqual(self.ple_inv_one.state_send,'1')
        self.assertEqual(self.ple_inv_one.date_ple,date.today())

        self.assertTrue(self.ple_inv_one.xls_filename_03)
        self.assertTrue(self.ple_inv_one.txt_filename_03)
        self.assertTrue(self.ple_inv_one.pdf_filename_03)
     
        
        

