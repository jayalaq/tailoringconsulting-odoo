from odoo.tests.common import TransactionCase

class TestInvoiceRetention(TransactionCase):

    def setUp(self):
        super(TestInvoiceRetention, self).setUp()

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

        self.payment_term = self.env['account.payment.term'].create({
            'name': '3% Saldo 30 Days',
            'line_ids': [
                (0, 0, {
                    'value_amount': 97.0,
                    'nb_days': 30,
                    'l10n_pe_is_detraction_retention': False,
                }),
                (0, 0, {
                    'value_amount': 3.0,
                    'nb_days': 1,
                    'l10n_pe_is_detraction_retention': True,
                }),
            ]
        })

    def test_invoice_with_retention(self):
        invoice = self.env['account.move'].create({
            'partner_id': self.partner.id,
            'move_type': 'out_invoice',
            'currency_id': self.currency_usd.id,  
            'invoice_line_ids': [(0, 0, {
                'product_id': self.product.id,
                'quantity': 1.0,
                'price_unit': 100.0,
            })],
            'invoice_payment_term_id': self.payment_term.id,  
            'agent_retention': True, 
            'multiplier_factor_field': 0.03,  
            'amount_field_advance': 3.0, 
            'debit_field_advance': 100.0,  
        })

        self.assertTrue(invoice, "La factura no se ha creado.")
        self.assertEqual(invoice.partner_id.name, 'Test Partner', "El cliente de la factura no es correcto.")
        self.assertEqual(invoice.state, 'draft', "El estado inicial de la factura debería ser 'draft'.")

        invoice.action_post()

        # Acceder directamente a las cuotas desde la factura
        cuotas = invoice.line_ids.filtered(lambda l: l.account_type == 'asset_receivable' and not l.l10n_pe_is_detraction_retention)

        # Verificar que la retención no aparezca como una cuota
        for cuota in cuotas:
            self.assertNotEqual(cuota.amount_currency, 3.0, "El monto de la retención no debe incluirse en el total de las cuotas.")

        # Verificar que la suma total de las cuotas no incluya la retención
        total_cuotas = sum(cuota.amount_currency for cuota in cuotas)
        self.assertNotEqual(total_cuotas, 100.0, "El total de las cuotas no debe incluir la retención.")

        print("------------- <<< TEST 3 >>> --------------------")