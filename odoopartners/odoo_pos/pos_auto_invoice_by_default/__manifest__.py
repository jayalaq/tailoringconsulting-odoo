{
    'name': 'POS Default Invoicing',
    'version': '17.0.1.0.1',
    'author': 'Ganemo',
    'website': 'https://www.ganemo.co/',
    'summary': 'Auto POS Invoice create from POS and send by email from point of sales automatic invoice',
    'description': """
     Auto POS Invoice create and send by email
    """,
    'category': 'Point of Sale',
    'depends': [
        'base',
        'point_of_sale',
    ],
    'data': [
        'views/pos_config_view.xml',
    ],
    'assets': {
        'point_of_sale._assets_pos': [
            'pos_auto_invoice_by_default/static/src/**/*',
        ],
    },
    'installable': True,
    'auto_install': False,
    'license': 'Other proprietary',
    'currency': 'USD',
    'price': 29.00,
    'module_type': 'official'
}