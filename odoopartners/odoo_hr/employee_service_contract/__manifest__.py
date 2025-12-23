{
    'name': 'Employee Service From Contracts',
    'version': '17.0.1.2.0',
    'author': 'Ganemo',
    'website': 'https://www.ganemo.co',
    'category': 'Human Resources/Payroll',
    'summary': 'Contract Management Module Integrated with Employee Service',
    'description': """
This module acts as an essential complement to the 'employee_service' module, providing a fluid and efficient interface to manage the connection and synchronization of data with employees' employment contracts.
""",
    'depends': [
        'employee_service',
        'hr_contract'
    ],
    'data': [
        'views/hr_employee_crons.xml',
        'views/hr_employee_views.xml'
    ],
    'application': False,
    'installable': True,
    'auto_install': False,
    'license': 'Other proprietary',
    'currency': 'USD',
    'price': 20.00
}
