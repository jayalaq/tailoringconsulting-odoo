{
    'name': 'Process AFP',
    'version': '17.0.1.1.4',
    'author': 'Ganemo',
    'website': 'https://www.ganemo.co',
    'summary': 'Generate the AFP files for the AFPnet declaration.',
    'description': """
    This module, Process AFP, generates the AFP files needed for AFPnet declarations, integrating with Odoo's payroll system to automate report and 
    certificate creation. It supports both enterprise and community versions of Odoo, allowing users to produce monthly AFP reports with accurate employee data.
    The module facilitates easy report generation, resulting in an Excel file for AFPnet submission, and ensures all necessary employee information, like 
    service start dates, is correctly included. It also provides robust error handling and detailed reporting features.
""",
    'depends': [
        'hr_localization_menu',
        'types_system_pension',
        'employee_service',
        'identification_type_employee',
        'personal_information',
        'setting_rules_payroll'
    ],
    'data': [
        'security/process_afp_security.xml',
        'security/ir.model.access.csv',
        'views/afp_interface_views.xml',
        'views/hr_salary_rule_views.xml'
    ],
    'application': False,
    'installable': True,
    'auto_install': False,
    'license': 'Other proprietary',
    'currency': 'USD',
    'price': 237.00,
    'module_type': 'official'
}
