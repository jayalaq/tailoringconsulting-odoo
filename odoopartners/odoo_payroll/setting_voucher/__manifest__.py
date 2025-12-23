{
    'name': 'Setting voucher',
    'version': '17.0.1.0.2',
    'author': 'Ganemo',
    'website': 'https://www.ganemo.co',
    'summary': 'This module creates a field called "additional certificate" in payroll.',
    'description': """
        A field was added to select the certificate or receipt related to the salary structure, which will be shown in the form when calculating. Screen reader support has been enabled.
    """,
    'category': 'Payroll',
    'depends': ['additional_fields_voucher'],
    'data': [
        'views/hr_views.xml',
        'views/reports.xml',
    ],
    'installable': True,
    'auto_install': False,
    'license': 'Other proprietary',
    'currency': 'USD',
    'price': 10.00,
    'module_type': 'official'
}
