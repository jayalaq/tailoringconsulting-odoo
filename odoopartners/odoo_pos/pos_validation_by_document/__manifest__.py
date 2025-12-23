{
    'name': 'POS Validation By Document',
    'version': '17.0.1.0.0',
    'author': 'Ganemo',
    'website': 'https://www.ganemo.co/',
    'category': 'Sales/Point of Sale',
    'summary': 'Add validations for the document type when placing an order from the POS',
    'description': """
Add validations for the document type when placing an order from the POS.
""",
    'depends': [
        'serie_and_correlative_pos',
        'invoice_validation_by_document'
    ],
    'data': [
        'views/res_config_settings_views.xml',
    ],
    'assets': {
        'point_of_sale._assets_pos': [
            'pos_validation_by_document/static/src/**/*',
        ],
    },
    'application': False,
    'installable': True,
    'auto_install': False,
    'license': 'Other proprietary',
    'currency': 'USD',
    'price': 60.00,
}
