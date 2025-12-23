{
    'name': 'Voucher CTS',
    'version': '17.0.1.0.2',
    'author': 'Ganemo',
    'website': 'https://www.ganemo.co',
    'live_test_url': 'https://www.ganemo.co/demo',
    'summary': 'Create the cts payment slip, and also add the CTS Settlement slip format',
    'description': 'Create the cts payment slip, and also add the CTS Settlement slip format',
    'category': 'Payroll',
    'depends': [
        'identification_type_employee',
        'employee_service',
        'setting_voucher',
        'legal_benefits_rule',
        'payment_conditions',
        'type_bank_accounts'
    ],
    'data': [
        'views/reports.xml'
    ],
    'installable': True,
    'auto_install': False,
    'license': 'Other proprietary',
    'currency': 'USD',
    'price': 20.00,
    'module_type': 'official'
}
