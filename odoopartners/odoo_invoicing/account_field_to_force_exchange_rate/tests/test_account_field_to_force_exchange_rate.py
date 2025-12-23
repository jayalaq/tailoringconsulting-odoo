from odoo.tests.common import TransactionCase

class TestAccountFieldToForceExchangeRate(TransactionCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.env.company.currency_id = cls.env['res.currency'].search([('name', '=', 'PEN')]).id
        cls.currency_id_usd = cls.env['res.currency'].search([
            ('name', '=', 'USD')
        ])
        cls.product = cls.env['product.product'].create({
            'name': 'Product',
            'standard_price': 600.0,
            'list_price': 147.0,
            'detailed_type': 'consu',
        })
        cls.price_unit = 100.0
        cls.exchange_rate = 4.0
        cls.forced_exchange_rate = 0.25

    def test_account_move(self):
        journal_id = self.env['account.journal'].create({
            'name': 'Diario Venta',
            'type': 'sale',
            'code': 'TestD',
            'currency_id': self.currency_id_usd.id,
        })
        res = self.env['account.move'].create({
                'move_type': 'out_invoice',
                'date': '2024-01-01',
                'journal_id': journal_id.id,
                'to_force_exchange_rate': self.forced_exchange_rate,
                'invoice_line_ids': [(0, 0, {
                    'product_id': self.product.id,
                    'price_unit': self.price_unit,
                    'tax_ids': [],
                })]
            })
        self.assertEqual(res.exchange_rate, self.exchange_rate)
        self.assertEqual(res.invoice_line_ids.credit, self.price_unit * self.exchange_rate)
        print('---------- PASSED ACCOUNT MOVE TEST OK ------------')

    def test_payment(self):
        res = self.env['account.payment'].create({
            'payment_type': 'inbound',
            'partner_type': 'customer',
            'to_force_exchange_rate': self.forced_exchange_rate,
            'currency_id': self.currency_id_usd.id,
            'amount': self.price_unit,
        })
        self.assertEqual(res.exchange_rate, self.exchange_rate)
        self.assertEqual(res.move_id.invoice_line_ids[0].debit, self.price_unit * self.exchange_rate)
        self.assertEqual(res.move_id.invoice_line_ids[1].credit, self.price_unit * self.exchange_rate)
        print('---------- PASSED ACCOUNT PAYMENT TEST OK ------------')