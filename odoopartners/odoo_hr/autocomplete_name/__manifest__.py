{
    'name': 'Autocomplete Name',
    'version': '17.0.1.0.0',
    'author': 'Ganemo',
    'website': 'https://www.ganemo.co',
    'category': 'Human Resources/Employees',
    'description': """
This module will automatically fill the name field of hr.employee with the fields of the personal_information module.
""",
    'summary': 'Automatically fills name field of hr.employee',
    'category': 'Payroll',
    'depends': ['personal_information'],
    'data': ['views/hr_employee_views.xml'],
    'installable': True,
    'auto_install': False,
    'application': False,
    'license': 'Other proprietary',
    'currency': 'USD',
    'price': 20.00,
}