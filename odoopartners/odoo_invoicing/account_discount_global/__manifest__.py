{
    'name': 'Account Discount Global',
    'version': '17.0.1.2.0',
    'author': 'Ganemo',
    'website': 'https://www.ganemo.co',
    'category': 'Accounting/Accounting',
    'module_type': 'official',
    'summary': 'This module creates a field called "Global discount %"',
    'description': """
In the sales invoice it shows a field called "Global Discount %" that calculates the 
percentage of global discount applied to the invoice, based on the negative lines
that correspond to the concept of global discount.
""",
    'depends': [
        'account'
    ],
    'data': [
        'views/account_move_views.xml',
        'views/product_template_views.xml'
    ],
    'application': False,
    'installable': True,
    'auto_install': False,
    'license': 'Other proprietary',
    'currency': 'USD',
    'price': 20.00
}
