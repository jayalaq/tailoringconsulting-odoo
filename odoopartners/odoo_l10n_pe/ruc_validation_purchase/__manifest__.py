{
    'name': 'Ruc Validation desde Compras',
    'version': '17.0.1.0.1',
    'author': 'Ganemo',
    'website': 'https://www.ganemo.co',
    'summary': 'It allows you to control whether a RUC is Active or Ingrained at the time of placing a purchase order.',
    'category': 'Accounting',
    'module_type': 'official',
    'depends': [
        'purchase',
        'ruc_validation_sunat',
        'l10n_country_filter'
    ],
    'data': ['views/purchase_views.xml'],
    'installable': True,
    'auto_install': False,
    'license': 'Other proprietary',
    'currency': 'USD',
    'price': 10.00
}
