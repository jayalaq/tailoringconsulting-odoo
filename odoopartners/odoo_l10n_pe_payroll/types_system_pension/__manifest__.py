{
    'name': 'Types System Pension',
    'version': '17.0.1.1.3',
    'author': 'Ganemo',
    'website': 'https://www.ganemo.co',
    'category': 'Human Resources/Payroll',
    'summary': 'Employee Pension System Allocation Module',
    'description': """
This module creates in the Location module a pension system type menu where all those registered in Peru are located. In addition, the commissions of each pension system and the corresponding limits can be managed. This information is displayed in hr.employee to assign to each worker and its calculation can be carried out on each payslip.
""",
    'depends': [
        'localization_menu',
        'hr_contract'
    ],
    'data': [
        'security/ir.model.access.csv',
        'data/pension_system_data.xml',
        'views/comis_system_pension_views.xml',
        'views/hr_employee_views.xml',
        'views/pension_system_menus.xml',
        'views/pension_system_views.xml',
        'views/tope_afp_menus.xml',
        'views/tope_afp_views.xml',
    ],
    'application': False,
    'installable': True,
    'auto_install': False,
    'license': 'Other proprietary',
    'currency': 'USD',
    'price': 20.0,
    'module_type': 'official'
}
