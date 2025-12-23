from odoo.tests.common import TransactionCase
from odoo.tests.common import Form
from datetime import datetime

class TestAccountExchangeCurrency(TransactionCase):

    def setUp(self):
        super(TestAccountExchangeCurrency, self).setUp()
        self.currency_usd = self.env['res.currency'].search([('name', '=', 'USD')])

    def test_validate_currency_date(self):
        date = datetime.now()
        currency_rate = self.env['res.currency.rate'].create({
            'name': date,
            'company_id': self.env.ref("base.main_company").id,
            'currency_id': self.currency_usd.id,
            'rate': 0.269970401720
        })
        account_form = self.env['account.move'].search([('date','=',currency_rate.name)])
        val_pen = round(account_form.exchange_rate,6)
        val_usd = round(1 / currency_rate.rate, 6)
        
        self.assertEqual(val_pen, val_usd)
        self.assertEqual(account_form._get_actual_currency_rate(),account_form.exchange_rate)
        