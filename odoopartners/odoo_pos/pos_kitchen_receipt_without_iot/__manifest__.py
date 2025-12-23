{
    'name': 'Print your order for the kitchen',
    'version': '17.0.1.0.0',
    'author': 'Ganemo',
    'website': 'https://www.ganemo.co',
    'summary': 'Allows you to send the order to the kitchen printer without using the IoT Box.',
    'category': 'Point of Sale',
    'live_test_url': 'https://www.ganemo.co/demo',
    'depends': ['pos_restaurant', 'pos_ticket_base_template'],
    'data': ['views/res_config_settings_views.xml'],
    'assets': {
        'point_of_sale._assets_pos': [
            'pos_kitchen_receipt_without_iot/static/src/**/*',
        ]
    },
    'installable': True,
    'auto_install': False,
    'license': 'Other proprietary',
    'currency': 'USD',
    'price': 72.00,
    'module_type': 'official',
}
