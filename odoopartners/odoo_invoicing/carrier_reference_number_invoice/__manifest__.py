{
    'name': 'Carrier reference number invoice',
    'version': '17.0.1.0.0',
    'author': 'Ganemo',
    'website': 'https://www.ganemo.co',
    'summary': '''
    Add a Field in the invoice to place the reference number related to the invoice.
    ''',
    'Description': '''
    The module creates a new field in the “Other information” tab called "remittance guide" in the path "accounting/customers/invoices" and when the move_type is equal to "out_invoice" and "out_refund" (customer invoices) and ( customer corrective invoices).
    ''',
    'category': 'Accounting',
    'depends': ['account'],
    'data': [
        'views/account_move.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': False,
    'license': 'Other proprietary',
    'currency': 'USD',
    'price': 10.00
}
