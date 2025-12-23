{
    'name': 'Life insurance management',
    'version': '17.0.1.0.0',
    'author': 'Ganemo',
    'website': 'https://www.ganemo.co',
    'category': 'Payroll',
    'summary': 'This module allows you to manage life insurance policies.',
    'description': """
    This module allows you to manage life insurance policies.
    """,
    'depends': [
        'localization_menu',
        'hr',
        'eps_process'
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/hr_employee_views.xml',
        'views/life_insurance_views.xml'
    ],
    'module_type': 'official',
    'application': False,
    'installable': True,
    'auto_install': False,
    'license': 'Other proprietary',
    'currency': 'USD',
    'price': 0.0
}
