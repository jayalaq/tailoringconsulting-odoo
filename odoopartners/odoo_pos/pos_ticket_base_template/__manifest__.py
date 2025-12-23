{
    'name': 'POS Ticket Base Template',
    'version': '17.0.1.3.0',
    'author': 'Ganemo',
    'website': 'https://www.ganemo.co',
    'category': 'Sales/Point of Sale',
    'summary': 'Technical module to centralize the overwriting of POS functionalities',
    'description': """
This module is technical with the purpose of creating a base module to centralize the overwriting of POS functionalities.
""",
    'depends': [
        'point_of_sale'
    ],
    'data': [
        'views/res_config_settings_views.xml'
    ],
    'assets': {
        'point_of_sale._assets_pos': [
            'pos_ticket_base_template/static/src/**/*',
        ],
    },
    'module_type': 'official',
    'application': False,
    'installable': True,
    'auto_install': False,
    'license': 'Other proprietary',
    'currency': 'USD',
    'price': 40.00
}
