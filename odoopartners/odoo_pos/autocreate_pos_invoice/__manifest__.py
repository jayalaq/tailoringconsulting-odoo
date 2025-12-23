{
    'name': 'Autocreate POS Invoice',
    'version': '17.0.1.4.0',
    'author': 'Ganemo',
    'website': 'https://www.ganemo.co',
    'summary': 'Automatic invoice creation in the POS',
    'description': """
This custom Odoo module enhances the functionality of the Point of Sale (POS) system, introducing new 
features and refining existing ones. The module introduces the following changes:

POS Configuration Enhancements:
    - 'Create Seat For Each Ticket' Option: Enables the creation of seats for each ticket in the POS.
    - 'Default User' Field: Allows setting a default user for POS operations.
    - 'Journal Tickets' Field: Introduces a 'Journal Tickets' field in POS configuration to specify the journal used for ticket-related transactions.

POS Order Customization:
    - 'Journal' Field: Adds a journal field to POS orders for better tracking of invoice.
""",
    'category': 'Sales/Point of Sale',
    'depends': [
        'pos_sale',
    ],
    'data': [
        'views/res_config_settings_views.xml',
        'views/pos_order_views.xml',
    ],
    'assets': {
        'point_of_sale._assets_pos': [
            'autocreate_pos_invoice/static/src/**/*',
        ],
    },
    'installable': True,
    'auto_install': False,
    'license': 'Other proprietary',
    'currency': 'USD',
    'price': 70.00
}
