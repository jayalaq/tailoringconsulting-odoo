{
    'name': 'Plantilla de Cheque USA',
    'version': '17.0.1.0.7',
    'author': 'Ganemo',
    'website': 'https://www.ganemo.co',
    'summary': 'Add Reconciliation Date Field',
    'Description': """
The USA_check_template module is intended to create a new check format.
    """,
    'module_type': 'official',
    'category': 'Accounting',
    'depends': [
        'account',
        'account_check_printing',
        'l10n_us'
    ],
    'data': [
        'data/us_check_printing.xml',
        'data/type_bill.xml',
        'report/print_check.xml',
        'report/print_check_usa.xml',
        'views/res_config_settings_views.xml',
    ],
    'assets': {
        'web.report_assets_common': [
            'USA_check_template/static/**/*',
        ],
    },
    'installable': True,
    'auto_install': False,
    'application': False,
    'license': 'Other proprietary',
    'currency': 'USD',
    'price': 80.00
}
