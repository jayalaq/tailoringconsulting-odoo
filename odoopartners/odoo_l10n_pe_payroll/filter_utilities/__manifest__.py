{
    'name': 'Filter Utilities',
    'version': '17.0.1.0.0',
    'author': 'Ganemo',
    'website': 'https://www.ganemo.co',
    'category': 'Payroll',
    'summary':'Filters on Utilities in the Payroll and Attendance Module',
    'description':""" 
This module describes the implementation of filters for utilities in the payroll and attendance module. It aims to streamline data management, enhance reporting accuracy, and improve overall system efficiency.
""",
    'depends': [
        'absence_manager',
        'payroll_utilities',
        'filter_payroll'
    ],
    'data': [
        'views/hr_attendance_views.xml',
        'views/hr_leave_views.xml',
        'views/hr_payslip_line_views.xml',
        'views/hr_payslip_worked_days_views.xml'
    ],
    'application': False,
    'installable': True,
    'auto_install': False,
    'license': 'Other proprietary',
    'currency': 'USD',
    'price': 20.00,
    'module_type': 'official'
}
