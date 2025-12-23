{
    'name': 'Voucher sending',
    'version': '17.0.1.0.3',
    'author': 'Ganemo',
    'website': 'https://www.ganemo.co',
    'category': 'Payroll',
    'summary': "Allows the automatic sending of tickets to the employee's emails",
    'depends': [
        'additional_fields_employee',
        'voucher_payroll',
        'portal'
    ],
    'data': [
        'security/ir.model.access.csv',
        'data/mail_template_inherit.xml',
        'data/mail_template_data.xml',
        'views/hr_views.xml',
        'static/src/xml/payslip_portal_template.xml',
        'static/src/xml/voucher_payrroll.xml'
    ],
    'installable': True,
    'auto_install': False,
    'license': 'Other proprietary',
    'currency': 'USD',
    'price': 0.0,
    'module_type': 'official'
}
