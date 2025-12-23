{
    'name': 'Efact: Advance - global discount',
    'version': '17.0.1.0.3',
    'author': 'Ganemo',
    'website': 'https://www.ganemo.co',
    'module_type': 'official',
    'summary': 'Efact: Advance - global discount',
    'description': """
Efact: Advance - global discount
    """,
    'category': 'Accounting/Localizations/EDI',
    'depends': ['l10n_pe_edocument'],
    'data': [
        'data/ubl_20_templates.xml',
        'views/account_move_views.xml',
        'views/product_template_views.xml',
    ],
    'application': False,
    'installable': True,
    'auto_install': False,
    'license': 'Other proprietary',
    'currency': 'USD',
    'price': 200.00
}
