from datetime import date
from odoo.tests.common import TransactionCase
from ..reports.report_txt_ple_3_18 import ReportTXTPLE

class TestWizardReportTxtPLE(TransactionCase):
    def setUp(self):
        self.obj = type('test', (object,), {
            'date_end': date(2023, 12, 31),
            'company_id': type('test', (object,), {'vat': '123456789'})(),
            'eeff_presentation_opportunity': '01',
            'state_send': '1'
        })()
         # Estructura correcta de los datos
        self.data = {
            0: [{
                'period': '20231231',
                'code': '09',
                'data_txt_dict': [
                    {
                        'code': '001',
                        'balance': 1000.00
                    }
                ],
                'indicador': '1'
            }]
        }
        self.report = ReportTXTPLE(self.obj, self.data)

    def test_get_content(self):
        content = self.report.get_content()
        expected_content = '20231231|09|001|1000.00|1|\r\n'
        self.assertEqual(content, expected_content)
        print('---------TEST GET CONTENT OK---------')

    def test_get_filename(self):
        filename = self.report.get_filename()
        expected_filename = 'LE12345678920231231031800011011.txt'
        self.assertEqual(filename, expected_filename)
        print("---------TEST GET FILENAME OK---------")