{
    'name': 'Print customer data on POS Ticket',
    'version': '17.0.1.0.1',
    'author': 'Ganemo',
    'website': 'https://www.ganemo.co/',
    'summary': 'Choose type of document when creating clients from POS',
    'description': """
     In the printed ticket of the POS add the customer information
    """,
    'category': 'Point of Sale',
    'depends': [
        'point_of_sale'
    ],
    'assets': {
        'point_of_sale._assets_pos': [
            'print_pos_customer/static/src/js/order_receipt.js',
            'print_pos_customer/static/src/xml/order_receipt.xml'
        ],
    },
    'installable': True,
    'auto_install': False,
    'license': 'Other proprietary',
    'currency': 'USD',
    'price': 0.00,
    'module_type': 'official'
}
