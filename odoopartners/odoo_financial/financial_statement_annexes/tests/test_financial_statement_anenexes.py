from odoo.tests.common import TransactionCase
from datetime import date, timedelta

dat = date.today()

class TestSaleDocumentType(TransactionCase):

    def setUp(self):
        super(TestSaleDocumentType, self).setUp()
        self.env['res.partner'].search([('name', '=', 'Test Supplier')]).unlink()
        self.supplier = self.env['res.partner'].create({'name': 'Test Supplier', 'supplier_rank': 1})
        self.company = self.env.ref("base.main_company")
        self.journal_purchase = self.env['account.journal'].search([('type', '=', 'purchase')], limit=1)

        self.account_1213000 = self.env['account.account'].search([('code','=', 1213000)])

        self.account_4212000 = self.env['account.account'].search([('code','=', 4212000)])

        self.data_report = {
            'date_start': dat,
            'date_end': dat,
            'xls_filename': 'Archivo',
            'xls_binary': False,
            'account_ids': [self.account_1213000.id, self.account_4212000.id],
        }
        self.document_type = self.env['l10n_latam.document.type'].search([('code', '=', '02')], limit=1)

    def create_wizard_report_model(self, report_data):
        model_wizard = self.env['wizard.report.financial'].create(report_data)
        return model_wizard

    def test_wizard_report_model(self):
        in_data = self.create_wizard_report_model(self.data_report)
        self.assertTrue(in_data)
        print('------------TEST OK - CREATE------------')

    def create_invoice(self, partner, date_invoice, amount, document_number):
        invoice = self.env['account.move'].create({
            'move_type': 'in_invoice',
            'partner_id': partner.id,
            'invoice_date': date_invoice,
            'journal_id': self.journal_purchase.id,
            'l10n_latam_document_number': document_number, 
            'invoice_line_ids': [(0, 0, {
                'name': 'Test Product',
                'quantity': 1,
                'price_unit': amount,
                'account_id': self.account_4212000.id,
            })],
            'l10n_latam_document_type_id': self.document_type.id
        })
        invoice.action_post()
        return invoice

    def register_payment(self, invoice, amount, payment_date):
        payment_method_line = self.env['account.payment.method.line'].search([
            ('payment_method_id', '=', self.env.ref('account.account_payment_method_manual_out').id),
            ('journal_id', '=', self.journal_purchase.id)
        ], limit=1)
        
        if not payment_method_line:
            payment_method_line = self.env['account.payment.method.line'].create({
                'journal_id': self.env['account.journal'].search([('type', '=', 'bank')], limit=1).id,
                'payment_method_id': self.env.ref('account.account_payment_method_manual_out').id,
            })

        payment = self.env['account.payment'].create({
            'payment_type': 'outbound',
            'partner_type': 'supplier',
            'partner_id': invoice.partner_id.id,
            'amount': amount,
            'date': payment_date,
            'payment_method_line_id': payment_method_line.id,
            'journal_id': self.env['account.journal'].search([('type', '=', 'bank')], limit=1).id,
        })
        payment.action_post()
        invoice.js_assign_outstanding_line(payment.line_ids[0].id)

    def test_conditions(self):
        invoice_1 = self.create_invoice(self.supplier, dat - timedelta(days=60), 1000, 'INV-001')
        self.register_payment(invoice_1, 1000, dat + timedelta(days=30))

        invoice_2 = self.create_invoice(self.supplier, dat - timedelta(days=60), 1000, 'INV-002')
        self.register_payment(invoice_2, 500, dat + timedelta(days=30))

        invoice_3 = self.create_invoice(self.supplier, dat - timedelta(days=60), 1000, 'INV-003')
        self.register_payment(invoice_3, 500, dat - timedelta(days=5))
        self.register_payment(invoice_3, 500, dat + timedelta(days=20))

        self.test_wizard_report_model()
        print('------------TEST OK - CONDITIONS------------')
