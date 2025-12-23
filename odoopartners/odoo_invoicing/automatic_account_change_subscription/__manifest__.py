{
    'name': 'Automatic Account Change Subscription',
    'version': '17.0.1.1.1',
    'author': 'Ganemo',
    'website': 'https://www.ganemo.co',
    'category': 'Accounting/Accounting',
    'summary': 'Change accounts receivable and payable from the invoice that is created in subscriptions',
    'description': """
The account receivable and payable for invoices changes depending on the currency and payment receipt type when you create the invoice from subscriptions.
""",
    'depends': [
        'sale_subscription',
        'automatic_account_change'
    ],
    'aplication': False,
    'installable': True,
    'auto_install': False,
    'license': 'Other proprietary',
    'currency': 'USD',
    'price': 12.00,
    'module_type': 'official',
}
