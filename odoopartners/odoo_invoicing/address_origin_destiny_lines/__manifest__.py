{
    'name': 'Address origin and destiny in the lines',
    'version': '17.0.1.0.1',
    'author': 'Ganemo',
    'website': 'https://www.ganemo.co',
    'category': 'All',
    'summary': 'this module will create the necessary fields to bring the address of origin and destination different from that of the client and company.',
    'description': """
This module will create 2 fields within the invoice line that can bring us an origin and destination address different from that of the client and that of the company.
""",
    'category': 'All',
    'depends': [
                'base',
                'account',
                ],
    'data': [
        'views/account_move_line_views.xml',
    ],
    'application': False,
    'installable': True,
    'auto_install': False,
    'license': 'Other proprietary',
    'currency': 'USD',
    'price': 0.00,
    'module_type': 'official'
}
