{
    'name': 'Financial Statement Annexes Enterprise',
    'version': '17.0.0.0.0',
    'author': 'Ganemo',
    'website': 'https://www.ganemo.co',
    'summary': 'Accounts receivable and payable reports with cut-off date and aging reports.',
    'category': 'Accounting',
    'depends': [
        'financial_statement_annexes',
        'account_reports',
    ],
    'assets': {
        'web.assets_backend': [
            'financial_statement_annexes_enterprise/static/src/**/*',
        ],
    },
    'installable': True,
    'auto_install': False,
    'license': 'Other proprietary',
    'currency': 'USD',
    'price': 120.00
}
