{
    'name': 'Holidays Accrual Advanced',
    'version': '17.0.1.0.1',
    'author': 'Ganemo',
    'website': 'https://www.ganemo.co',
    'category': 'Payroll',
    'summary': 'Customizable Missing/Assignments Calculator',
    "description": """
This module has been created with the purpose of having an assignment calculator which you configure according to the need for the calculation that you need to program automatically,This calculator is located in the absence / approvals / assignments.

Module create the field:
- accumulation method (accrual_method).
""",
    'depends': [
        'hr_holidays'
    ],
    'data': [
        'security/ir.model.access.csv',
        'security/holidays_accrual_advanced_ir_rule.xml',
        'wizards/hr_leave_allocation_accrual_calculator_views.xml',
        'wizards/hr_leave_allocation_accrual_calculator_accruement_views.xml',
        'views/hr_leave_allocation_menus.xml',
        'views/hr_leave_allocation_views.xml',
        'views/hr_leave_allocation_accruement_views.xml'
    ],
    'installable': True,
    'auto_install': False,
    'application': False,
    'license': 'Other proprietary',
    'currency': 'USD',
    'price': 20.00,
    'module_type': 'official',
}
