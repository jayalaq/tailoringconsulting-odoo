{
    'name': 'Select Invoice Format POS',
    'version': '17.0.1.1.0',
    'author': 'Ganemo',
    'website': 'https://www.ganemo.co',
    'summary': 'Select the invoice to print at the POS',
    'description': """
This module adds the invoice format that you want to use for the POS and adds a button 
at the end of the payment to be able to manually print said configured invoice.
""",
    'category': 'Sales/Point of Sale',
    'depends': [
        'pos_ticket_base_template',
    ],
    'data': [
        'views/res_config_settings_views.xml',
    ],
    'assets': {
        'point_of_sale._assets_pos': [
            'select_invoice_format_pos/static/src/**/*',
        ],
    },
    'application': False,
    'installable': True,
    'auto_install': False,
    'license': 'Other proprietary',
    'currency': 'USD',
    'price': 40.00
}
