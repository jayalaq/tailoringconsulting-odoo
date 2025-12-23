{
    'name': 'Account field to Force Exchange Rate',
    'version': '17.0.2.0.7',
    'author': 'Ganemo',
    'website': 'https://www.ganemo.co',
    'category': 'Accounting/Accounting',
    'summary': 'This module will create a field to force the exchange rate',
    'description': """
The field Force to exchange rate will change the exchange rate to custom one rate in payments and invoices
""",
    'depends': [
        'account_exchange_currency',
        'payment_term_lines',
    ],
    'data': [
        'views/account_move_views.xml',
        'views/account_payment_views.xml',
    ],
    'application': False,
    'installable': True,
    'auto_install': False,
    'license': 'Other proprietary',
    'currency': 'USD',
    'price': 100.00,
    'module_type': 'official',
}
