{
    'name': 'Payroll utilites',
    'version': '17.0.1.0.2',
    'author': 'Ganemo',
    'website': 'https://www.ganemo.co',
    'category': 'Payroll',
    'summary': 'Allows you to manage the payment of benefits to employees.',
    'description': 'Allows you to manage the payment of benefits to employees.',
    'depends': [
        'setting_rules_payroll',
        'hr_holidays',
        'payroll_fields',
        'absence_day',
        'hr_localization_menu'
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/data_utilities_views.xml',
        'views/hr_leave_type_views.xml',
        'views/hr_payslip_views.xml',
        'views/hr_salary_rule_views.xml',
        'views/hr_work_entry_type_views.xml',
        'views/hr_payroll_structure_views.xml'
    ],
    'application': False,
    'installable': True,
    'auto_install': False,
    'license': 'Other proprietary',
    'currency': 'USD',
    'price': 20.00,
    'module_type': 'official'
}
