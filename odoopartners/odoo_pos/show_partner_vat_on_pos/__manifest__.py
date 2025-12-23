{
    'name': 'Show partner VAT on POS',
    'version': '17.0.1.0.0',
    'author': 'Ganemo',
    'website': 'https://www.ganemo.co',
    'category': 'Point Of Sale',
    'summary': 'Displays the customers identification number, in the POS customer list',
    'description': """
Displays the customer's identification number, in the POS customer list. When searching by document number, it makes it easier to identify the customer being searched for.
""",
    'depends': [
        'point_of_sale'
    ],
    'assets': {
        'point_of_sale._assets_pos': [
            'show_partner_vat_on_pos/static/src/xml/templates.xml',
        ]
    },
    'application': False,
    'installable': True,
    'auto_install': False,
    'license': 'Other proprietary',
    'currency': 'USD',
    'price': 23.00,
    'module_type': 'official'
}
