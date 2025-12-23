{
    'name': 'Customize Later Delivery',
    'version': '17.0.1.0.0',
    'author': 'Ganemo',
    'website': 'https://www.ganemo.co',
    'summary': 'Customize Later Delivery.',
    'description': """
        Customize Later Delivery.
    """,
    'category': 'Sales/Point of Sale',
    'depends': [
        'point_of_sale'
    ],
    'data': [
        'views/res_config_settings_views.xml'
    ],
    'assets': {
        'point_of_sale._assets_pos': [
            'customize_later_delivery_for_pos/static/src/**/*',
        ],
    },
    'auto_install': False,
    'installable': True,
    'license': 'Other proprietary',
    'currency': 'USD',
    'price': 50.00,
}
