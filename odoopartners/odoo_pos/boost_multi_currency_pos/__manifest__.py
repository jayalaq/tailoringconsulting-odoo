{
    'name': 'POS Multi Currency',
    'version': '17.0.1.0.3',
    'author': 'Ganemo',
    'website': 'https://www.ganemo.co',
    'live_test_url': 'https://www.ganemo.co/demo',
    'summary': 'Payment with multiple currencies from Point of sale Interface',
    'description': """
This module is allow to pay with multiple currencies from POS Interface.
    """,
    'module_type': 'official',
    'category': 'Sales/Point of Sale',
    'depends': [
        'account',
        'point_of_sale',
        'web'
    ],
    'data': [
        'data/res_currency_rate.xml',
        'views/pos_order_views.xml',
        'views/res_config_settings_views.xml',
    ],
    'assets': {
        'point_of_sale._assets_pos': [
            'boost_multi_currency_pos/static/src/**/*',
        ],
    },
    'application': False,
    'installable': True,
    'auto_install': False,
    'license': 'Other proprietary',
    'currency': 'USD',
    'price': 100.00,
    'post_init_hook': 'post_init_hook',
    # 'uninstall_hook': 'uninstall_hook',
}
