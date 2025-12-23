{
    'name': 'Base Spot',
    'version': '17.0.1.0.0',
    'author': 'Ganemo',
    'website': 'https://www.ganemo.co',
    'live_test_url': 'https://www.ganemo.co/demo',
    'summary': """
        Add fields for legal deductions.
    """,
    'Description': '''
        Create additional fields on purchase invoices that allow you to identify if an invoice is affected by legal deductions, the type of deduction, 
        the payment date of the deduction and the payment operation code of the deduction.
    ''',
    'category': 'All',
    'depends': ['localization_menu'],
    'data': [
        'data/account_spot_detraction_data.xml',
        'views/account_move_views.xml',
        'views/account_spot_views.xml'
    ],
    'installable': True,
    'auto_install': False,
    'application': False,
    'license': 'Other proprietary',
    'currency': 'USD',
    'price': 10.00
}
