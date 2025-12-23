{
    'name': 'Filter payroll',
    'version': '17.0.1.0.2',
    'author': 'Ganemo',
    'website': 'https://www.ganemo.co',
    'category': 'Payroll',
    'summary': 'This module adds in Payroll and Attendance the CTS and Gratification filters.',
    'description': """
Adds the CTS / Gratuities filters to the days analysis in payroll. 
CTS / Gratuities filters are added in the attendance module.
    """,
    'depends': [
        'absence_manager',
        'automatic_leave_type',
        'payroll_fields'
    ],
    'data': [
        'views/hr_attendance_views.xml',
        'views/hr_leave_type_views.xml',
        'views/hr_leave_views.xml',
        'views/hr_payslip_views.xml',
        'views/hr_payslip_worked_days_views.xml',
        'views/hr_work_entry_type_views.xml'
    ],
    'application': False,
    'installable': True,
    'auto_install': False,
    'license': 'Other proprietary',
    'currency': 'USD',
    'price': 20.00,
    'module_type': 'official'
}
