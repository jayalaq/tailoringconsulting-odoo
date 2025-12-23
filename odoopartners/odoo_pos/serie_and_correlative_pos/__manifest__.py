{
    'name': 'Serie And Correlative POS',
    'version': '17.0.1.2.0',
    'author': 'Ganemo',
    'website': 'https://www.ganemo.co',
    'category': 'Sales/Point of Sale',
    'summary': 'Types of documents in the POS',
    'description': """
This module allows you to configure the document types to use when creating the invoice or receipt in the POS.
""",
    'depends': [
        'autocreate_pos_invoice',
        'l10n_latam_invoice_document'
    ],
    'data': [
        'views/res_config_settings_views.xml',
        'views/pos_order_views.xml'
    ],
    'assets': {
        'point_of_sale._assets_pos': [
            'serie_and_correlative_pos/static/src/**/*',
        ],
    },
    'application': False,
    'installable': True,
    'auto_install': False,
    'license': 'Other proprietary',
    'currency': 'USD',
    'price': 60.00
}
