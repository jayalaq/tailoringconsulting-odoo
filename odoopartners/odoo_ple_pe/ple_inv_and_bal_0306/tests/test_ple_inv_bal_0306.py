from odoo.tests import tagged
from odoo.tests.common import TransactionCase
from odoo.exceptions import AccessError, ValidationError
from datetime import date

@tagged('-at_install', 'post_install')
class TestPleInvAndBal0306(TransactionCase):

    @classmethod
    def setUpClass(self):
        super(TestPleInvAndBal0306, self).setUpClass()
        self.ple_inv_bal_one = self.env['ple.report.inv.bal.one']
        self.ple_report_inv_bal_06 = self.env['ple.report.inv.bal.06']
        self.ple_report_inv_bal_06_line = self.env['ple.report.inv.bal.line.06']

        self.company_temp = self.env['res.company'].create({
            'name': 'Company test',
        })


    def create_ple_inv_bal_one(self):
        temp_ple_inv_bal_one = self.ple_inv_bal_one.create({
            'financial_statements_catalog': '01',
            'eeff_presentation_opportunity': '01',
            'company_id': self.company_temp.id,
            'date_start': date(2023, 7, 11),
            'date_end': date(2023, 1, 15),
            'state': 'draft',
            'state_send': '0',
        })
        return temp_ple_inv_bal_one

    def test_ple_inv_bal_one_action_generate_excel(self):
        ple_inv_bal_one_temp = self.create_ple_inv_bal_one()
        ple_inv_bal_one_temp.action_generate_excel()
        self.assertRaises(ValidationError, ple_inv_bal_one_temp.action_generate_excel())
        self.assertIsNone(ple_inv_bal_one_temp.action_generate_excel())
        print("-----------------TEST PLE INV BAL ONE ACTION GENERATE OK-----------------")

    def create_ple_report_inv_bal_06(self):
        temp_ple_report_inv_bal_06 = self.ple_report_inv_bal_06.create({
            'company_id': self.company_temp.id,
            'date_start': date(2023, 7, 11),
            'date_end': date(2023, 8, 15),
            'state': 'draft',
            'state_send': '0',
            'date_ple': date(2023, 8, 15),
            'financial_statements_catalog': '01',
            'eeff_presentation_opportunity': '01',
        })
        return temp_ple_report_inv_bal_06

    def create_ple_report_inv_bal_06_line(self):
        temp_ple_report_inv_bal_06_line = self.ple_report_inv_bal_06_line.create({
            'name':'periodo prueba',
            'document_name':'2356',
            'correlative':'5437',
            'type_document_debtor':'type_document_debtor',
            'tax_identification_number':'1',
            'business_name':'Juan Perez',
            'type_document':'ruc',
            'number_serie':'53453532',
            'number_document':'4324234',
            'date_of_issue':'29/12/2023',
            'provisioned_invoice':'23',
            'provision_amount':1000.0,
            'state':'True',
        })

        return temp_ple_report_inv_bal_06_line

    def test_ple_report_inv_bal_06_action_generate_excel(self):
        ple_report_inv_bal_06_temp = self.create_ple_report_inv_bal_06()
        ple_report_inv_bal_06_line_temp = self.create_ple_report_inv_bal_06_line()

        ple_report_inv_bal_06_temp.write({'line_ids': [(6, 0, ple_report_inv_bal_06_line_temp.ids)]})
        ple_report_inv_bal_06_line_temp.write({'ple_report_inv_val_06_id': ple_report_inv_bal_06_temp.id})

        ple_report_inv_bal_06_temp.action_generate_excel()
        year, month, day = ple_report_inv_bal_06_temp.date_end.strftime('%Y/%m/%d').split('/')

        self.assertRaises(ValidationError, ple_report_inv_bal_06_temp.action_generate_excel())
        self.assertIsNone(ple_report_inv_bal_06_temp.action_generate_excel())

        self.assertEqual(ple_report_inv_bal_06_temp.xls_filename, f'Libro_Estimación cobranza dudosa_{year}{month}.xlsx')
        self.assertEqual(ple_report_inv_bal_06_temp.pdf_filename, f'Libro_Estimación cobranza dudosa_{year}{month}.pdf')
        print("-----------------TEST PLE REPORT INV BAL 06 ACTION GENERATE OK-----------------")