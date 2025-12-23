{
    'name': 'Process PLAME',
    'version': '17.0.1.0.2',
    'author': 'Ganemo',
    'website': 'https://www.ganemo.co',
    'description': "",
    'depends': [
        'additional_fields_voucher',
        'hr_localization_menu',
        'filter_payroll',
        'types_system_pension',
        'identification_type_employee'
    ],
    'data': [
        'data/hr_employee_category_data.xml',
        'data/plame.lines.csv',
        'security/ir.model.access.csv',
        'views/base_views.xml',
        'views/plame_files_views.xml',
        'views/plame_lines_views.xml',
        'views/structure_views.xml'
    ],
    'installable': True,
    'auto_install': False,
    'license': 'Other proprietary',
    'currency': 'USD',
    'price': 0.00,
    'module_type': 'official'
}
