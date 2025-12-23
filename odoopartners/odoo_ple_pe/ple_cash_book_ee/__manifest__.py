{
    'name': 'Register of Cash and banks PLE - SUNAT (Perú) - Enterprise',
    'version': '17.0.1.0.0',
    'author': 'Ganemo',
    'website': 'https://www.ganemo.co/ple',
    'category': 'Accounting',
    'summary': 'Register of Cash and banks PLE - SUNAT (Perú) - Enterprise',
    'description': """
Generates the electronic register of Cash and Banks in .txt file, ready to present to SUNAT via electronic book program (PLE - SUNAT).This is a mandatory e-book for companies that are required to keep complete accounting.
 """,
    'depends': [
        'ple_cash_book', 
        'account_accountant'
    ],
    'data': [
        'views/account_bank_statement_line_views.xml',
        'views/account_payment_register_views.xml',
        'views/account_payment_views.xml'
    ],
    'application': False,
    'installable': True,
    'auto_install': False,
    'license': 'Other proprietary',
    'currency': 'USD',
    'price': 160.00,
    'module_type': 'official'
}
