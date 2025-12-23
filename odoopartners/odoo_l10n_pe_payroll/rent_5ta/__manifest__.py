{
    'name': 'Renta de quinta',
    'version': '17.0.1.0.9',
    'author': 'Ganemo',
    'website': 'https://www.ganemo.co',
    'summary': 'It is in charge of creating a complete model for the calculation of fifth rent, considering all the parameters established by SUNAT',
    'description': """
    This module, "rent_5ta," creates a comprehensive model for calculating the fifth category income tax (Renta de 5ta) in accordance with SUNAT's parameters.
    It integrates with Odoo's payroll system to manage tax rates and generate necessary fields for accurate tax computation. The module supports the creation
    and management of various income types and projections, providing detailed options for calculating taxes based on current, previous month, or contract
    information. Additionally, it features manual adjustment fields and recalculation capabilities to ensure precise and up-to-date tax information, making it
    suitable for both community and enterprise versions of Odoo.
""",
    'depends': [
        'basic_rule',
        'additional_fields_voucher',
        'employee_service_contract',
        'hr_work_entry_contract_enterprise',
    ],
    'data': [
        'data/hr_data.xml',
        'data/payroll_projection_exception_data.xml',
        'data/payroll_projection_data.xml',
        'security/ir.model.access.csv',
        'views/hr_views.xml',
        'views/payroll_projection_views.xml',
        'views/rate_fifth_rent_views.xml',
        'views/reports.xml',
        'views/wizards.xml',
        'views/wizard_recalc.xml'
    ],
    'application': False,
    'installable': True,
    'auto_install': False,
    'license': 'Other proprietary',
    'currency': 'USD',
    'price': 0.00,
    'module_type': 'official'
}
