from odoo.tests.common import TransactionCase
from odoo.exceptions import ValidationError
from datetime import date
import re


class TestPleInvBal13(TransactionCase):

    def setUp(self):
        super(TestPleInvBal13, self).setUp()
        self.ple_inv_bal_one = self.env['ple.report.inv.bal.one']
        self.company = self.env['res.company'].create({
            'name': 'Company for test',
        })

    def create_ple_inv_bal_one(self):
        return self.ple_inv_bal_one.create({
            'company_id': self.company.id,
            'state_send': '0',
            'eeff_presentation_opportunity': '01',
            'financial_statements_catalog': '02',
            'xls_filename_313': 'Test_Excel_File',
            'txt_filename_313': 'Test_Text_File',
            'pdf_filename_313': 'Test_PDF_File',
            'date_start': date(2023, 1, 1),
            'date_end': date(2023, 1, 31),
        })
    
    def test_ple_inv_bal_lines_data(self):
        ple_inv_bal_lines = self.env['ple.report.inv.bal.line.13'].create({
            'move': 'Factura de Prueba',
            'ple_correlative': '123456',
            'l10n_latam_identification_type_id': '06',
            'vat': '12345678901',
            'partner': 'Empresa de Prueba',
            'balance': 1500.0,
            'date': '15/07/2023',
        })

        self.assertEqual(ple_inv_bal_lines.move, 'Factura de Prueba')
        self.assertEqual(ple_inv_bal_lines.ple_correlative, '123456')
        self.assertEqual(ple_inv_bal_lines.l10n_latam_identification_type_id, '06')
        self.assertEqual(ple_inv_bal_lines.vat, '12345678901')
        self.assertEqual(ple_inv_bal_lines.partner, 'Empresa de Prueba')
        self.assertEqual(ple_inv_bal_lines.balance, 1500.0)
        self.assertEqual(ple_inv_bal_lines.date, '15/07/2023')

    def test_action_generate_excel(self):

        ple_inv_bal_one = self.create_ple_inv_bal_one()
        ple_inv_bal_one.action_generate_excel()        
        
        self.assertTrue(ple_inv_bal_one.xls_filename_313)
        self.assertTrue(ple_inv_bal_one.xls_binary_313)
        self.assertTrue(ple_inv_bal_one.txt_filename_313)
        self.assertTrue(ple_inv_bal_one.txt_binary_313)
        self.assertTrue(ple_inv_bal_one.pdf_filename_313)
        self.assertTrue(ple_inv_bal_one.pdf_binary_313)
        self.assertFalse(ple_inv_bal_one.line_ids_313)
