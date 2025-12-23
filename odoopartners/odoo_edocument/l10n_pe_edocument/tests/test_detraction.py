from odoo.tests.common import TransactionCase

class TestInvoiceWithDiscount(TransactionCase):

    def setUp(self):
        super(TestInvoiceWithDiscount, self).setUp()

        self.partner = self.env['res.partner'].create({
            'name': 'Test Partner',
            'vat': '20551583041',  
            'country_id': self.env.ref('base.pe').id,  
        })

        self.product = self.env['product.product'].create({
            'name': 'Test Product',
            'list_price': 100.0,
            'standard_price': 80.0,
            'global_discount': True,  
        })

        
        self.currency_usd = self.env['res.currency'].search([('name', '=', 'USD')], limit=1)
        if not self.currency_usd:
            self.currency_usd = self.env['res.currency'].create({
                'name': 'USD',
                'symbol': '$',
                'rounding': 0.01,
            })

    def test_create_invoice_with_discount(self):
        invoice = self.env['account.move'].create({
            'partner_id': self.partner.id,
            'move_type': 'out_invoice',
            'currency_id': self.currency_usd.id,  
            'invoice_line_ids': [(0, 0, {
                'product_id': self.product.id,
                'quantity': 1.0,
                'price_unit': 85.0,
                'discount': 10.0,  
            })]
        })

        self.assertTrue(invoice, "La factura no se ha creado.")
        self.assertEqual(invoice.partner_id.name, 'Test Partner', "El cliente de la factura no es correcto.")
        self.assertEqual(invoice.state, 'draft', "El estado inicial de la factura debería ser 'draft'.")

        invoice.action_post()

        product_discount = any(line.product_id.global_discount for line in invoice.invoice_line_ids)
        self.assertTrue(product_discount, "El producto de la factura no tiene descuento global aplicado.")

        self.assertEqual(invoice.currency_id.name, 'USD', "La moneda de la factura no es USD.")

        print("--------- <<<<<<   TEST 2 >>>>>> ---------")
