{
    'name': 'Employee Service',
    'version': '17.0.1.1.0',
    'author': 'Ganemo',
    'website': 'https://www.ganemo.co',
    'category': 'Human Resources/Payroll',
    'summary': 'Manage services for your employees',
    'description': """ 
This module is designed to manage and organize information related to the services offered by the company to its employees.This module provides functionalities such as service request tracking schedule management, access to internal policies, shared resource reservations and others.
""",
    'depends': [
        'hr', 
        'hr_contract'
    ],
    'data': [
        'views/hr_employee_views.xml'
    ],
    'application': False,
    'installable': True,
    'auto_install': False,
    'license': 'Other proprietary',
    'currency': 'USD',
    'price': 20.00,
    'module_type': 'official'
}
