{
    'name': 'Type bank accounts',
    'version': '17.0.1.0.3',
    'author': 'Ganemo',
    'website': 'https://www.ganemo.co',
    'category': 'Payroll',
    'summary': 'Adds 4 bank account types.',
    'description': "This module adds 4 employee bank account types field to the payments section in the private information tab.",
    'depends': ['hr'],
    'data': [
        'views/hr_employee_views.xml',
        'views/res_partner_bank_views.xml',
    ],
    'installable': True,
    'auto_install': False,
    'license': 'Other proprietary',
    'currency': 'USD',
    'price': 20.00,
    'module_type': 'official'
}
