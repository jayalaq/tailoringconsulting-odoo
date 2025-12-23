from odoo import Command, fields
from odoo.addons.account.tests.common import AccountTestInvoicingCommon
from odoo.tests.common import tagged


@tagged('post_install', '-at_install')
class TestAccountDiscountGlobal(AccountTestInvoicingCommon):

    def test_discount_global_compute(self):

        discount = 10

        product_discount_tmpl = self.env['product.template'].with_context(allowed_company_ids=self.env.company.ids).create({
            'name': 'discount',
            'company_id': self.company_data['company'].id,
            'global_discount': True,
        })
        product_discount = self.env['product.product'].create({
            'product_tmpl_id': product_discount_tmpl.id,
            'taxes_id': [Command.set(self.tax_sale_a.ids)],
            'supplier_taxes_id': [Command.set(self.tax_purchase_a.ids)],
            'active': True,
        })

        move = self.env['account.move'].create({
            'move_type': 'in_invoice',
            'date': '2019-01-01',
            'invoice_date': '2019-01-01',
            'partner_id': self.partner_a.id,
            'invoice_cash_rounding_id': self.cash_rounding_b.id,
            'invoice_payment_term_id': self.pay_terms_a.id,
            'invoice_line_ids': [
                (0, 0, {
                    'product_id': self.product_a.id,
                    'price_unit': 100.0,
                    'tax_ids': [(6, 0, self.product_a.supplier_taxes_id.ids)],
                    'product_uom_id':  self.product_a.uom_id.id,
                }),
                (0, 0, {
                    'product_id': product_discount.id,
                    'price_unit': -10.0,
                    'tax_ids': [(6, 0, self.product_a.supplier_taxes_id.ids)],
                    'product_uom_id':  self.product_b.uom_id.id,
                }),
            ],
        })

        self.assertEqual(move.discount_percent_global, discount)
        print('-----PASSED TEST------')
