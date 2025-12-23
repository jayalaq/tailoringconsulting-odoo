{
    'name': 'l10n pe fields for classic format invoice',
    'version': '17.0.1.0.3',
    'author': 'Ganemo',
    'website': 'https://www.ganemo.co',
    'category': 'All',
    'summary': 'This module will be used to make the classic invoice compatible for the Peruvian localization. ',
    'description': """
This module will be used to make the classic invoice compatible for the Peruvian localization.
    """,
    "depends": [
        'account',
        'l10n_pe',
        'classic_format_invoice',
        'qr_code_on_sale_invoice',
        'account_exchange_currency'
    ],
    'data': [
        'views/report_invoice.xml',
        'views/report_templates.xml',
        'views/ticket_template.xml'
    ],
    'application': False,
    'installable': True,
    'auto_install': False,
    'license': 'Other proprietary',
    'currency': 'USD',
    'price': 20.00,
    'module_type': 'official'
}
