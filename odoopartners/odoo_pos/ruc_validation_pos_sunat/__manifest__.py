{
    'name': 'Check RUC and DNI from the POS',
    'version': '17.0.1.0.1',
    'author': 'Ganemo',
    'live_test_url': 'https://www.ganemo.co/demo',
    'website': 'https://www.ganemo.co',
    'summary': 'Consultation and autocompletion of RUC and DNI from the POS.',
    'category': "Point Of Sale",
    'depends': [
        'ruc_validation_sunat',
        'l10n_pe_pos'
    ],
    'assets': {
        'point_of_sale._assets_pos': [
            'ruc_validation_pos_sunat/static/src/**/*',
        ],
    },
    'auto_install': False,
    'installable': True,
    'license': "Other proprietary",
    'currency': "USD",
    'price': 99.00,
    'module_type': 'official'
}
