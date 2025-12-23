{
    'name': 'Judicial retention fields',
    'version': '17.0.1.0.3',
    'author': 'Ganemo',
    'website': 'https://www.ganemo.co',
    'category': 'Payroll',
    'summary': 'Allows management of withholdings by judicial process of employees',
    'description': """
This module allows the management of withholdings by judicial process of employees.
    """,
    'depends': [
        'hr',
        'l10n_latam_base',
        'additional_fields_voucher',
        'payment_conditions',
        'type_bank_accounts'
    ],
    'data': [
        'views/report.xml',
        'views/hr_employee_views.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': False,
    'license': 'Other proprietary',
    'currency': 'USD',
    'price': 20.0
}
