{
    'name': 'Payroll fields',
    'version': '17.0.1.0.1',
    'author': 'Ganemo',
    'website': 'https://www.ganemo.co',
    'category': 'Human Resources/Payroll',
    'summary':'This module creates a payroll month field which controls which month each payroll corresponds to, additionally creates the menu analysis of days, entries, and payroll for better control of importing information and payroll analysis.',
    'description': """
This module has been created to create a field called payroll month (date_start_dt). in the employee's payslips (hr.paylis) in order to control which month each payroll corresponds to, in addition to this it also creates in the report tab the payroll analysis entries
"Entry Analysis, Payroll Analysis and Worked Days Analysis" for better control of the import of payroll information and analysis.
    """,
    'depends': [
        'additional_fields_employee',
        'hr_payroll'],
    'data': [
        'security/hr_rules.xml',
        'views/hr_payslip_input_views.xml',
        'views/hr_payslip_line_views.xml',
        'views/hr_payslip_views.xml',
        'views/hr_payslip_worked_days_views.xml',
        'views/hr_payslip_input_menus.xml',
        'views/hr_payslip_worked_days_menus.xml',
        'views/hr_payslip_line_menus.xml',
    ],
    'installable': True,
    'auto_install': False,
    'license': 'Other proprietary',
    'currency': 'USD',
    'price': 20.00
}
