{
    "name": "Employee certificate for employee",
    'version': '17.0.1.1.1',
    'author': 'Ganemo',
    'website': 'https://www.ganemo.co',
    'category': 'Payroll',
    'summary': 'Enables the issuance of work certificates for employees',
    "description": """
    This module facilitates the task of issuing employment certificates, allowing you to generate documents that detail the employment 
    relationship of a specific employee. Relevant information, such as work start and departure dates, is automatically incorporated into the certificate.
    """,
    "depends": [
        'hr_payroll',
        'base',
        'employee_service',
        'payment_conditions',
        'additional_fields_voucher',
        'identification_type_employee',
    ],
    "data": [
        'views/certificate_view.xml',
        'report/certification_employee_report.xml',
        'report/certification_employee_template.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': False,
    'license': 'Other proprietary',
    'currency': 'USD',
    'price': 20.00
}
