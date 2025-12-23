{
    'name': 'Financial Statement Annexes',
    'version': '17.0.1.1.1',
    'author': 'Ganemo',
    'website': 'https://www.ganemo.co',
    'summary': 'Accounts receivable and payable reports with cut-off date and aging reports.',
    'description': """
    Add the annexes menu in accounting reports, along with all the logic to allow accounts receivable and payable reports with cut-off date and aging reports
    """,
    'category': 'Accounting',
    'depends': ['add_reconcile_date'],
    'data': [
        'security/ir.model.access.csv',
        'views/wizard_report_financial_views.xml'
    ],
    'installable': True,
    'auto_install': False,
    'module_type': 'official',
    'license': 'Other proprietary',
    'currency': 'USD',
    'price': 120.00
}
