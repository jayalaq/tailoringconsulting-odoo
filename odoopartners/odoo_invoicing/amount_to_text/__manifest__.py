{
    'name': 'Amount To Text',
    'version': '17.0.1.3.0',
    'author': 'Ganemo',
    'website': 'https://www.ganemo.co',
    'category': 'Accounting/Accounting',
    'summary': 'Convert the total amount into letters',
    'description': """
This module creates a function in the "account.move" model that converts the
total amount of the invoice (amount_total) to text in spanish.

This module serves as help to other modules (mostly modules that create invoice reports)
to complete the total amount in letters.
""",
    'depends': [
        'account'
    ],
    'application': False,
    'installable': True,
    'auto_install': False,
    'license': 'Other proprietary',
    'currency': 'USD',
    'price': 20.00
}
