from odoo import fields
from odoo.tests import tagged
from odoo.addons.account.tests.common import AccountTestInvoicingCommon


@tagged('amount_to_text', 'post_install', '-at_install', '-standard')
class TestAmountToText(AccountTestInvoicingCommon):

    def test_amount_to_text_zero_cents(self):
        """
        Verifica la conversión de la cantidad total sin centavos.
        """
        move = self.init_invoice(
            move_type='out_invoice',
            partner=self.partner_a,
            invoice_date=fields.Date.from_string('2019-01-01'),
            amounts=[1400.00],
            post=True,
        )

        amount_text = move._amount_to_text()
        expected_result = 'MIL CUATROCIENTOS Y 00/100 DOLLARS'
        self.assertEqual(amount_text, expected_result)

        # Cambio de moneda a PEN
        move.write({'currency_id': self.env.ref('base.PEN')})
        amount_text = move._amount_to_text()
        expected_result = 'MIL CUATROCIENTOS Y 00/100 SOLES'
        self.assertEqual(amount_text, expected_result)

    def test_amount_to_text_negative_amount(self):
        """
        Verifica la conversión de una cantidad total negativa.
        """
        move = self.init_invoice(
            move_type='out_invoice',
            partner=self.partner_a,
            invoice_date=fields.Date.from_string('2019-01-01'),
            amounts=[-1400.00],
            post=False,
        )

        amount_text = move._amount_to_text()
        expected_result = 'MENOS MIL CUATROCIENTOS Y 00/100 DOLLARS'
        self.assertEqual(amount_text, expected_result)

        # Cambio de moneda a PEN
        move.write({'currency_id': self.env.ref('base.PEN')})
        amount_text = move._amount_to_text()
        expected_result = 'MENOS MIL CUATROCIENTOS Y 00/100 SOLES'
        self.assertEqual(amount_text, expected_result)

    def test_amount_to_text_decimal_amount(self):
        """
        Verifica la conversión de una cantidad total con decimales.
        """
        move = self.init_invoice(
            move_type='out_invoice',
            partner=self.partner_a,
            invoice_date=fields.Date.from_string('2019-01-01'),
            amounts=[1411.25],
            post=True,
        )

        amount_text = move._amount_to_text()
        expected_result = 'MIL CUATROCIENTOS ONCE Y 25/100 DOLLARS'
        self.assertEqual(amount_text, expected_result)

        # Cambio de moneda a PEN
        move.write({'currency_id': self.env.ref('base.PEN')})
        amount_text = move._amount_to_text()
        expected_result = 'MIL CUATROCIENTOS ONCE Y 25/100 SOLES'
        self.assertEqual(amount_text, expected_result)

    def test_amount_to_text_large_amount(self):
        """
        Verifica la conversión de una cantidad total grande.
        """
        move = self.init_invoice(
            move_type='out_invoice',
            partner=self.partner_a,
            invoice_date=fields.Date.from_string('2019-01-01'),
            amounts=[9876543.21],
            post=True,
        )

        amount_text = move._amount_to_text()
        expected_result = 'NUEVE MILLONES OCHOCIENTOS SETENTA Y SEIS MIL QUINIENTOS CUARENTA Y TRES Y 21/100 DOLLARS'
        self.assertEqual(amount_text, expected_result)

        # Cambio de moneda a PEN
        move.write({'currency_id': self.env.ref('base.PEN')})
        amount_text = move._amount_to_text()
        expected_result = 'NUEVE MILLONES OCHOCIENTOS SETENTA Y SEIS MIL QUINIENTOS CUARENTA Y TRES Y 21/100 SOLES'
        self.assertEqual(amount_text, expected_result)
