{
    'name': 'Holiday Process',
    'version': '17.0.1.0.3',
    'author': 'Ganemo',
    'website': 'https://www.ganemo.co',
    'category': 'Payroll',
    'summary': 'It allows us to manage the process of sale-purchase vacations in odoo.',
    'description': """
        Create a tab in employees called "Vacation and allowances" which shows us a summary of the worker's earned, taken and pending vacations. 
        Additionally, create a button to generate workers' assignments and thus be able to proportionally calculate workers' vacations.
    """,
    'depends': [
        'employee_service_contract',
        'holidays_accrual_advanced',
        'hr_payroll',
        'hr_work_entry_holidays',
        'automatic_leave_type'
    ],
    'data': [
        'security/ir.model.access.csv',
        'security/hr_holidays_security.xml',
        'data/hr_work_entry_type_data.xml',
        'data/hr_leave_type_data.xml',
        'views/holiday_generator_wizard.xml',
        'views/holiday_petition_wizard.xml',
        'views/holiday_update_wizard.xml',
        'views/hr_employee_views.xml',
        'views/hr_leave_allocation_views.xml',
        'views/hr_leave.xml',
    ],
    'application': False,
    'installable': True,
    'auto_install': False,
    'license': 'Other proprietary',
    'currency': 'USD',
    'price': 20.00,
    'module_type': 'official',
}