{
    'name': 'AFP Commissions',
    'version': '17.0.1.4.1',
    'author': 'Ganemo',
    'website': 'https://www.ganemo.co',
    'category': 'Payroll',
    'summary': 'Monthly search for AFP percentage types.',
    'description': '''
Allows you to keep updated the percentages of the different types of AFP and the maximum amount of AFP for payroll calculation.
''',
    'depends': ['account', 'types_system_pension', 'api_data_token'],
    'data': ['data/ir_cron.xml',
             'views/pension_system_view.xml',
             ],
    'installable': True,
    'auto_install': False,
    'application': False,
    'license': 'Other proprietary',
    'currency': 'USD',
    'module_type': 'official',
    'price': 20.00
}
