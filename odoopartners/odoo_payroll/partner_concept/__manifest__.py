{
    'name': 'Partner Concept',
    'version': '17.0.1.2.0',
    'author': 'Ganemo',
    'website': 'https://www.ganemo.co',
    'category': 'Human Resources/Payroll',
    'summary': 'Manage salary concepts individually for employees',
    'description': """
This module allows you to manage salary concepts individually for employees.
""",
    'depends': [
        'hr_payroll'
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/hr_partner_concept_views.xml',
        'views/hr_employee_views.xml'
    ],
    'application': False,
    'installable': True,
    'auto_install': False,
    'license': 'Other proprietary',
    'currency': 'USD',
    'price': 20.00
}
