from odoo.tests.common import TransactionCase

class TestCreditNoteWithReference(TransactionCase):

    def setUp(self):
        super(TestCreditNoteWithReference, self).setUp()

        self.partner = self.env['res.partner'].create({
            'name': 'Test Partner',
            'vat': '20551583041',
            'country_id': self.env.ref('base.pe').id,
        })
        self.product = self.env['product.product'].create({
            'name': 'Test Product',
            'list_price': 100.0,
            'standard_price': 80.0,
        })

        self.currency_usd = self.env['res.currency'].search([('name', '=', 'USD')], limit=1)
        if not self.currency_usd:
            self.currency_usd = self.env['res.currency'].create({
                'name': 'USD',
                'symbol': '$',
                'rounding': 0.01,
            })

        # Crear una factura original para ser referenciada
        self.original_invoice = self.env['account.move'].create({
            'partner_id': self.partner.id,
            'move_type': 'out_invoice',
            'currency_id': self.currency_usd.id,
            'invoice_line_ids': [(0, 0, {
                'product_id': self.product.id,
                'quantity': 1.0,
                'price_unit': 100.0,
            })],
        })
        self.original_invoice.action_post()

    def test_create_credit_note_with_reference(self):
        # Crear la nota de crédito con referencia a la factura original
        credit_note = self.env['account.move'].create({
            'partner_id': self.partner.id,
            'move_type': 'out_refund', 
            'currency_id': self.currency_usd.id,
            'invoice_line_ids': [(0, 0, {
                'product_id': self.product.id,
                'quantity': 1.0,
                'price_unit': 100.0, 
            })],
            'origin_number': self.original_invoice.name,
            'l10n_latam_document_type_id': self.env.ref('l10n_pe.document_type07').id,  # Tipo de documento de Nota de Crédito
        })

        credit_note.action_post()

        self.assertEqual(
            credit_note.origin_number,
            self.original_invoice.name,
            "La nota de crédito no tiene la referencia correcta al documento original."
        )

        print("--------- <<<<<<   TEST 5  >>>>>> ---------")
