{
    'name': 'POS Product Return',
    'version': '17.0.1.2.0',
    'author': 'Ganemo',
    'website': 'https://www.ganemo.co',
    'category': 'Sales/Point of Sale',
    'summary': 'Show receipt number and type in the POS',
    'description': """
This module adds the number and type of receipt in the POS and also saves the information of the credit notes in the order.
""",
    'depends': [
        'point_of_sale',
        'l10n_latam_invoice_document'
    ],
    'assets': {
        'point_of_sale._assets_pos': [
            'pos_product_return/static/src/**/*',
        ],
    },
    'application': False,
    'installable': True,
    'auto_install': False,
    'license': 'Other proprietary',
    'currency': 'USD',
    'price': 50.00
}
