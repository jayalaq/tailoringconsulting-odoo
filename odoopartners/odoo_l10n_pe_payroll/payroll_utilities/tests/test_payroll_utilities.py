from odoo.tests.common import TransactionCase
from odoo.exceptions import ValidationError


class TestPayrollUtilities(TransactionCase):

    def test_compute_fields(self):
        data_util = self.env['data.utilities'].create({
            'date_from': '2024-01-01',
            'date_to': '2024-12-31',
            'annual_rent_before_tax': 2000000,
            'percent': 0.1,
            'difference': 0.0,
            'is_active': True
        })

        data_util.compute_fields()
        self.assertEqual(data_util.amount, 200000)
        print('------TEST COMPUTE PAYROLL UTILITIES OK--------------')

    def test_check_is_active(self):
        data_util1 = self.env['data.utilities'].create({
            'date_from': '2024-01-01',
            'date_to': '2024-12-31',
            'annual_rent_before_tax': 10000,
            'percent': 0.5,
            'is_active': True
        })
        with self.assertRaises(ValidationError):
            data_util2 = self.env['data.utilities'].create({
                'date_from': '2024-01-01',
                'date_to': '2024-12-31',
                'annual_rent_before_tax': 20000,
                'percent': 0.8,
                'is_active': True
            })
        print('------TEST CHECK PAYROLL UTILITIES OK--------------')

    def test_date_validation(self):
        with self.assertRaises(ValidationError):
            data_util = self.env['data.utilities'].create({
                'date_from': '2024-12-31',
                'date_to': '2024-01-01',
                'annual_rent_before_tax': 10000,
                'percent': 0.5,
            })
            data_util.compute_fields()

        with self.assertRaises(ValidationError):
            data_util = self.env['data.utilities'].create({
                'date_from': '2024-01-01',
                'date_to': '2025-01-01',
                'annual_rent_before_tax': 10000,
                'percent': 0.5,
            })
            data_util.compute_fields()

        print('------TEST DATE VALIDATION OK--------------')

    def test_name_get(self):
        data_util = self.env['data.utilities'].create({
            'date_from': '2024-01-01',
            'date_to': '2024-12-31',
            'annual_rent_before_tax': 10000,
            'percent': 0.5,
            'is_active': True
        })

        name = data_util.name_get()[0][1]
        expected_name = '2024-12-31-2024-01-01 - ACTIVO'
        self.assertEqual(name, expected_name)

        data_util.is_active = False
        name = data_util.name_get()[0][1]
        expected_name = '2024-12-31-2024-01-01'
        self.assertEqual(name, expected_name)

        print('------TEST NAME GET OK--------------')