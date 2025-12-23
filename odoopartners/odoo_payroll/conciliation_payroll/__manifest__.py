{
    'name': 'Conciliation payroll',
    'version': '17.0.1.0.1',
    'author': 'Ganemo',
    'website': 'https://www.ganemo.co',
    'summary': 'Generates the global accounting entry to reconcile the payslip of the payroll calculation. It also changes the status of the payslip to paid.',
    'description': """
Generates the global accounting entry to reconcile the payslip of the payroll calculation. It also changes the status of the payslip to paid.
""",
    'depends': [
        'hr_payroll_account',
        'txt_bank_lo_pe',
    ],
    'data': [
        'views/hr_massive_payment_views.xml',
        'views/hr_payslip_views.xml'
    ],
    'application': False,
    'installable': True,
    'auto_install': False,
    'module_type': 'official',
    'license': 'Other proprietary',
    'currency': 'USD',
    'price': 10.00
}
