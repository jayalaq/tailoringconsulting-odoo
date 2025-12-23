{
    'name': 'Holiday rules',
    'version': '17.0.1.0.1',
    'author': 'Ganemo',
    'website': 'https://www.ganemo.co',
    'category': 'Payroll',
    'summary':'This module installs the rules for calculating vacations',
    'description': """ 
This module automates and optimizes vacation calculation using 20 specific salary rules, ensuring accurate management of employees vacation entitlements. It includes automatic compensation calculations for untaken vacations, with exceptions for certain types of contracts, and is compatible with both the Enterprise and Community versions of Odoo, offering flexibility and efficiency in payroll administration.
""",
    'depends': [
        'basic_rule',
        'holiday_process',
        'absence_day'
    ],
    'data': [
        'data/hr_payroll_structure_data.xml',
        'data/hr_payslip_input_type_data.xml',
        'data/hr_salary_rule_category_data.xml',
        'data/hr_salary_rule_data.xml',
    ],
    'application': False,
    'installable': True,
    'auto_install': False,
    'license': 'Other proprietary',
    'currency': 'USD',
    'price': 20.00,
    'module_type': 'official'
}
