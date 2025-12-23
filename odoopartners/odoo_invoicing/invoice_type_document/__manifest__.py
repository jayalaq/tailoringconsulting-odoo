{
    'name': 'Place invoice data in reconciliations',
    'version': '17.0.1.0.2',
    'author': 'Ganemo',
    'website': 'https://www.ganemo.co',
    'category': 'Accounting',
    'summary': 'Automatic Document Data in Reconciliations',
    'description':"""
This module will allow us to place the type of document, document series and payment receipt number automatically through the reconciliations.
""",
    'depends': [
        'account', 
        'l10n_latam_invoice_document'
    ],
    'data': [
        'views/account_move_line_views.xml',
        'views/account_move_views.xml',
    ],
    'application': False,
    'installable': True,
    'auto_install': False,
    'license': 'Other proprietary',
    'currency': 'USD',
    'price': 25.00,
    'module_type': 'official',

}
