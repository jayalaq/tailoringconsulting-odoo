{
    'name': 'Voucher LBS',
    'version': '17.0.1.0.2',
    'author': 'Ganemo',
    'website': 'https://www.ganemo.co',
    'summary': 'Create the payment slip for Settlement of social benefits, and also add the form of settlement of social benefits',
    'description': """
This module allows you to create the payment slip for the settlement of social benefits and add the corresponding format for the settlement of these benefits. Facilitates the management and documentation of employee benefits, ensuring that all necessary details are included and presented in a clear and organized manner.
    """,
    'depends': [
        'holiday_field_payroll',
        'identification_type_employee',
        'additional_fields_payroll',
        'additional_fields_voucher',
        'legal_benefits_rule',
    ],
    'data': [
        'data/section_lbs_data.xml',
        'security/ir.model.access.csv',
        'views/hr_views.xml',
        'views/section_lbs_views.xml',
        'views/reports.xml'
    ],
    'application': False,
    'installable': True,
    'auto_install': False,
    'module_type': 'official',
    'license': 'Other proprietary',
    'currency': 'USD',
    'price': 20.00
}
