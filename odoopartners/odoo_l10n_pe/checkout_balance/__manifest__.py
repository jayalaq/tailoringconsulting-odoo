{
    'name': 'Checkout balance',
    'version': '17.0.1.0.0',
    'author': 'Ganemo',
    'website': 'https://www.ganemo.co',
    'summary': 'Creates the trial balance report that includes the income statement by nature and by function.',
    'category': 'Accounting',
    'module_type': 'official',
    'depends': ['account_reports'],
    'data': [
        'data/checkout_balance_report.xml',
        'views/account_group_views.xml'
    ],
    'installable': True,
    'auto_install': False,
    'license': 'Other proprietary',
    'currency': 'USD',
    'price': 30.00
}
