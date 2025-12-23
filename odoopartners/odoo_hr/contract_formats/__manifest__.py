{
    'name': 'Contract Formats',
    'version': '17.0.1.0.1',
    'author': 'Ganemo',
    'website': 'https://www.ganemo.co',
    'category': 'Payroll',
    'summary': 'Allows you to generate employee contract templates',
    'description': """
    Allows you to generate employee contract templates
    """,
    'depends': [
        'additional_fields_voucher',
        'identification_type_employee'
    ],
    'data': [
        'data/hr_contract_data.xml',
        'data/cron.xml',
        'reports/hr_contract_report.xml',
        'reports/hr_contract_template.xml',
        'views/mail_template_preview_views.xml',
        'views/hr_contract_views.xml'
    ],
    'application': False,
    'installable': True,
    'auto_install': False,
    'license': 'Other proprietary',
    'currency': 'USD',
    'price': 20.00,
    'module_type': 'official'
}
