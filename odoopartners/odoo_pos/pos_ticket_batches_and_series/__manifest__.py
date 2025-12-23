{
    'name': 'Pos ticket batches and series',
    'version': '17.0.1.0.0',
    'author': 'Ganemo',
    'website': 'https://www.ganemo.co',
    'category': 'Point of Sale',
    'summary': 'This module allows you to add the batch number or serial number',
    'description':"""  
This module allows adding the lot number or serial number at the bottom of the printed invoice receipt. With this functionality, each product that has a serial number or lot number can display this information clearly and in detail on the receipt, providing greater traceability and control over the sold products.
""",
    'depends': [
        'pos_ticket_format_invoice',
    ],
    'data': [
        'reports/ticket_template.xml',
    ],
    'assets': {
        'web.report_assets_common': [
            'pos_ticket_batches_and_series/static/src/css/main.css',
        ]
    },
    'application': False,
    'installable': True,
    'auto_install': False,
    'license': 'Other proprietary',
    'currency': 'USD',
    'price': 95.00,
    'module_type': 'official'
}
