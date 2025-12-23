from odoo.tests.common import TransactionCase

class TestInvoiceWithRetention(TransactionCase):

    def setUp(self):
        super(TestInvoiceWithRetention, self).setUp()

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

        # Crear un término de pago de 30 días 
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

    def test_create_invoice_with_USD(self):
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

        
        self.assertTrue(invoice.agent_retention, "La factura no tiene retención aplicada.")
        self.assertEqual(float(invoice.multiplier_factor_field), 0.03, "El factor de retención no es del 3%.")
        self.assertEqual(invoice.currency_id.name, 'USD', "La moneda de la factura no es USD.")

        
        self.assertEqual(invoice.invoice_payment_term_id.name, '3% Saldo 30 Days', "El plazo de pago no es de 30 días.")

        print("--------- <<<<<<   TEST 4 >>>>>> ---------")
