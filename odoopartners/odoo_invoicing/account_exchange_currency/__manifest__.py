{
    'name': 'Account Exchange Currency',
    'version': '17.0.1.0.0',
    'author': 'Ganemo',
    'website': 'https://www.ganemo.co',
    'category': 'Accounting/Accounting',
    'summary':'Allows you to store the exchange rate value on the invoice which is updated based on the date and currency',
    'description': """
This module allows you to store the exchange rate value on the invoice, which is updated based on the date and currency. This exchange rate is the same one Odoo uses to convert values to the company's currency, but we make it visible on the invoice and store it, allowing it to be easily retrieved in a report. We recommend that modules that require knowing the exchange rate of Invoices for reporting use this module as a dependency.
""",
    'depends': [
        'account'
    ],
    'data': [
        'views/account_move_views.xml'
    ],
    'application': False,
    'installable': True,
    'auto_install': False,
    'license': 'Other proprietary',
    'currency': 'USD',
    'price': 20.00
}
