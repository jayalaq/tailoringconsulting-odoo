{
    'name': 'Legal benefits rule',
    'version': '17.0.1.0.0',
    'author': 'Ganemo',
    'website': 'https://www.ganemo.co',
    'category': 'Payroll',
    'summary':'This module creates the salary rules for social benefits',
    'description': """ 
This module creates the salary rules for social benefits such as vacations, cts, gratuity and liquidation.
""",
    'depends': [
        'compensated_hours',
        'holiday_rule'
    ],
    'data': [
        'data/hr_work_entry_type_data.xml',
        'data/hr_payroll_structure_data.xml',
        'data/hr_payslip_input_type_data.xml',
        'data/hr_salary_rule_category_data.xml',
        'data/hr_salary_rule_data.xml'
    ],
    'application': False,
    'installable': True,
    'auto_install': False,
    'license': 'Other proprietary',
    'currency': 'USD',
    'price': 20.00,
    'module_type': 'official'
}
