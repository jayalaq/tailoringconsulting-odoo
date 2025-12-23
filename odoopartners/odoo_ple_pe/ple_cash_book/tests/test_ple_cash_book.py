from odoo import fields
from odoo.tests.common import TransactionCase

class TestAccountPayment(TransactionCase):

    def setUp(self):
        super(TestAccountPayment, self).setUp()
        self.partner = self.env['res.partner'].create({
            'name': 'Test Partner',
            'email': 'test@example.com',
            'country_id': self.env.ref('base.pe').id
        })
        self.product = self.env['product.product'].create({
            'name': 'Test Product',
            'list_price': 100.0,
            'standard_price': 50.0,
            'type': 'service',
        })
        self.payment_method = self.env['payment.methods.codes'].create({
            'code': '003',
            'description': 'Test Payment Method',
        })
        self.bank_journal = self.env['account.journal'].create({
            'name': 'Test Bank Journal',
            'type': 'bank',
            'code': 'TBJ',
            'l10n_latam_use_documents': True,
            'company_id': self.env.company.id,
        })
        self.purchase_journal = self.env['account.journal'].create({
            'name': 'Test Purchase Journal',
            'type': 'purchase',
            'code': 'TPJ',
            'company_id': self.env.company.id,
        })
        self.sale_journal = self.env['account.journal'].create({
            'name': 'Test Sale Journal',
            'type': 'sale',
            'code': 'TSJ',
            'company_id': self.env.company.id,
        })
        self.company = self.env.ref('base.main_company')
        self.company.country_id = self.env.ref('base.pe').id

        self.document_type = self.env['l10n_latam.document.type'].search([('country_id.code', '=', 'PE')], limit=1)

    def test_account_payment(self):
        # Crear factura de compra
        purchase_invoice = self.env['account.move'].create({
            'partner_id': self.partner.id,
            'move_type': 'in_invoice',
            'invoice_date': fields.Date.today(),
            'l10n_latam_document_number': 'B001-000001',
            'journal_id': self.purchase_journal.id,
            'invoice_line_ids': [(0, 0, {
                'product_id': self.product.id,
                'quantity': 1,
                'price_unit': 100.0,
            })],
            'l10n_latam_document_type_id': self.document_type.id,
        })
        purchase_invoice.action_post()

        # Crear factura de venta
        sale_invoice = self.env['account.move'].create({
            'partner_id': self.partner.id,
            'move_type': 'out_invoice',
            'invoice_date': fields.Date.today(),
            'l10n_latam_document_number': 'F001-000001',
            'journal_id': self.sale_journal.id,
            'invoice_line_ids': [(0, 0, {
                'product_id': self.product.id,
                'quantity': 1,
                'price_unit': 100.0,
            })],
            'l10n_latam_document_type_id': self.document_type.id,
        })
        sale_invoice.action_post()

        # Registrar factura de compra
        purchase_payment = self.env['account.payment'].create({
            'partner_id': self.partner.id,
            'amount': 100.0,
            'payment_type': 'outbound',
            'partner_type': 'supplier',
            'journal_id': self.bank_journal.id,
            'means_payment_id': self.payment_method.id,
        })
        purchase_payment.action_post()

        # Registrar factura de venta
        sale_payment = self.env['account.payment'].create({
            'partner_id': self.partner.id,
            'amount': 100.0,
            'payment_type': 'inbound',
            'partner_type': 'customer',
            'journal_id': self.bank_journal.id,
            'means_payment_id': self.payment_method.id,
        })
        sale_payment.action_post()

        try:
            libro = self.env['account.libro'].create({})
            libro.action_emit()
            self.assertFalse(libro.message_post_ids, "book emitted")
        except Exception as e:
            self.fail(f"book emission failed: {e}")
