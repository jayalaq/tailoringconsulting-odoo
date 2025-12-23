from odoo.tests.common import TransactionCase
from odoo.exceptions import ValidationError
from datetime import datetime, timedelta
from odoo import fields

class TestAccountMove(TransactionCase):

    def setUp(self):
        super(TestAccountMove, self).setUp()
        self.account_move_model = self.env['account.move']
        self.partner_model = self.env['res.partner']
        self.document_type_model = self.env['l10n_latam.document.type']

        self.country_id = self.env.ref('base.pe').id 

        self.document_type = self.document_type_model.create({
            'name': 'Factura',
            'code': '01',
            'require_validation_ruc': True,
            'country_id': self.country_id  
        })

        self.env.company.write({
            'token_api_ruc': 'YOUR_VALIDATION_TOKEN'  # Reemplaza con el token adecuado
        })

        self.partner = self.partner_model.create({
            'name': 'Test Partner',
            'l10n_latam_identification_type_id': self.env.ref('l10n_pe.it_RUC').id,
            'vat': '20512345670',  # Un RUC válido para pruebas
            'condition_contributor_sunat': 'HABIDO',
            'state_contributor_sunat': 'ACTIVO',
        })

        self.invoice = self.account_move_model.create({
            'partner_id': self.partner.id,
            'invoice_date': fields.Date.today() - timedelta(days=15),
            'l10n_latam_document_type_id': self.document_type.id,
            'move_type': 'in_invoice',
        })
        print("---------------- SET UP -------------------")

    def test_action_ruc_validation_sunat(self):
        self.invoice.action_ruc_validation_sunat()

        self.assertEqual(self.invoice.active_and, 'done')
        self.assertIn('Al momento de realizar la Consulta RUC del comprobante', self.invoice.message_response)
        print("---------------- SET 1 -------------------")
    
    def test_action_ruc_validation_sunat_with_invalid_date(self):
        self.invoice.invoice_date = None

        with self.assertRaises(ValidationError):
            self.invoice.action_ruc_validation_sunat()
        print("---------------- SET 2 -------------------")

    def test_action_post(self):
        self.invoice.active_and = 'done'
        self.invoice.action_post()

        invoice = self.account_move_model.create({
            'partner_id': self.partner.id,
            'invoice_date': fields.Date.today() - timedelta(days=15),
            'l10n_latam_document_type_id': self.document_type.id,
            'move_type': 'in_invoice',
        })

        with self.assertRaises(ValidationError):
            invoice.action_post()
        print("---------------- SET 3 -------------------")


















































