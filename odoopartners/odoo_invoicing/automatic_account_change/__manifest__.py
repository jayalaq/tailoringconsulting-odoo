{
    'name': 'Cambiar Cuenta Corriente Facturas',
    'version': '17.0.1.1.0',
    'author': 'Ganemo',
    'website': 'https://www.ganemo.co',
    'category': 'Accounting/Accounting',
    'summary': 'International financial management invoices.',
    'description': 'The account receivable and payable of the invoices, changes according to the currency and the type of proof of payment',
    'depends': ['account'],
    'data': [
        'security/ir.model.access.csv',
        'views/account_views.xml',
    ],
    'installable': True,
    'auto_install': False,
    'license': 'Other proprietary',
    'currency': 'USD',
    'price': 8.00,
}
