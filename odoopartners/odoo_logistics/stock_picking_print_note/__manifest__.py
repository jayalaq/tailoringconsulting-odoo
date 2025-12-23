{
    'name': 'Print note on Warehouse guide',
    'version': '17.0.1.4.0',
    'author': 'Ganemo',
    'website': 'https://www.ganemo.co',
    'summary': 'Includes Inventory Transfer Notes in printed format',
    'description':"""
In the format for printing the delivery voucher, the Notes field and fields 
for the signature of those involved in the transfer are added.
""",
    'category': 'Warehouse',
    'depends': [
        'stock',
    ],
    'data': ['static/src/xml/qweb_templates.xml'],
    'installable': True,
    'auto_install': False,
    'application': False,
    'license': 'Other proprietary',
    'currency': 'USD',
    'price': 5.00
}
