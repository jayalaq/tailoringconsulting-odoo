from odoo.exceptions import UserError
from odoo.tests.common import TransactionCase


class TestDocumentInSupplierInvoice(TransactionCase):

    @classmethod
    def setUpClass(cls):
        super(TestDocumentInSupplierInvoice, cls).setUpClass()
        cls.product = cls.env['product.product'].create({
            'name': 'Product',
            'standard_price': 600.0,
            'list_price': 147.0,
            'detailed_type': 'consu',
        })
        cls.fac = cls.env['l10n_latam.document.type'].create({
            'name': 'Factura',
            'doc_code_prefix': 'F',
            'country_id': cls.env.ref('base.pe').id
        })
        cls.bol = cls.env['l10n_latam.document.type'].create({
            'name': 'Boleta',
            'doc_code_prefix': 'B',
            'country_id': cls.env.ref('base.pe').id
        })
        cls.l10n_latam_identification_type_01 = cls.env['l10n_latam.identification.type'].search([
            ('name', '=', 'VAT'),
        ])
        cls.partner = cls.env['res.partner'].create({
            'name': "Partner PE",
            'l10n_latam_identification_type_id': cls.l10n_latam_identification_type_01.id,
            'country_id': cls.env.ref('base.pe').id,
        })

    def test_post_in_invoice(self):

        self.l10n_latam_identification_type_01.invoice_validation_document = [self.bol.id]

        move = self.env['account.move'].create({
            'move_type': 'out_invoice',
            'date': '2024-01-01',
            'partner_id': self.partner.id,
            'l10n_latam_document_type_id': self.fac.id,
            'invoice_line_ids': [(0, 0, {
                'product_id': self.product.id,
                'price_unit': 100.0,
                'tax_ids': [],
            })]
        })
        with self.assertRaises(
            UserError, 
            msg='El tipo de documento que está intentando publicar, NO es el permitido, por favor verificar si es el que es el que está permitido'
        ):
            move.action_post()
        print('TEST POST INVOICE OK')