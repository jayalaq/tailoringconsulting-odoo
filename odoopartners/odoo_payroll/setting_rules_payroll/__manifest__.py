{
    'name': 'Setting Rules Payroll',
    'version': '17.0.1.1.0',
    'author': 'Ganemo',
    'website': 'https://www.ganemo.co',
    'category': 'Human Resources/Payroll',
    'summary': 'Create tab in salary rules',
    'description': """
This module has been designed with the purpose of extending the configuration actions 
in the salary rules model (hr.salary.rule), so it creates a tab called "configuration".
""",
    'depends': [
        'hr_payroll'
    ],
    'data': [
        'views/hr_salary_rule_views.xml'
    ],
    'application': False,
    'installable': True,
    'auto_install': False,
    'license': 'Other proprietary',
    'currency': 'USD',
    'price': 20.00
}
