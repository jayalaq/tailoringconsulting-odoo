from odoo.tests import TransactionCase, tagged
from odoo.exceptions import UserError
import base64
import io
import zipfile

@tagged('post_install', '-at_install')
class TestAccountMoveQRCode(TransactionCase):

    def setUp(self):
        super(TestAccountMoveQRCode, self).setUp()

        self.company = self.env['res.company'].create({
            'name': 'Test Company',
            'vat': '123456789',
            'security_lead': 0.0, 
        })

        self.journal = self.env['account.journal'].create({
            'name': 'Test Sales Journal',
            'type': 'sale',
            'code': 'TESTSALES',
            'company_id': self.company.id,
        })

        self.partner = self.env['res.partner'].create({
            'name': 'Test Partner',
            'vat': '20551583041',
            'company_id': self.company.id,
            'l10n_latam_identification_type_id': self.env.ref('l10n_pe.it_RUC').id,
        })

        self.invoice = self.env['account.move'].create({
            'move_type': 'out_invoice',
            'partner_id': self.partner.id,
            'invoice_date': '2024-08-19',
            'name': 'F001-00000001',
            'company_id': self.company.id,
            'amount_tax': 18.0,
            'amount_total': 118.0,
        })

        print("------<<<<< SET UP >>>>>------")

    def test_create_data_qr_code(self):
        """Prueba para verificar la generación correcta del código QR"""
        qr_code_data = self.invoice.create_data_qr_code()

        expected_template = '{ruc}|{document_type_name}|{series}|{correlative}|{total_igv}|{total_amount}|' \
                            '{date_invoice}|{document_type_name_user}|{document_number_user}|{signature_hash}|\r\n'

        expected_data = expected_template.format(
            ruc='123456789',
            document_type_name=0, #self.partner.l10n_latam_identification_type_id.l10n_pe_vat_code,
            series='F001',
            correlative='00000001',
            total_igv=0.0,
            total_amount=118.0,
            date_invoice='19-08-2024',
            document_type_name_user=self.partner.l10n_latam_identification_type_id.l10n_pe_vat_code,
            document_number_user='20551583041',
            signature_hash='',
        )

        self.assertEqual(qr_code_data, expected_data, "El código QR generado no es el esperado.")
        print("------<<<<< TEST QR >>>>>------")

