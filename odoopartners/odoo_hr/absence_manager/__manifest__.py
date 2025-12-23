{
    'name': 'Absence manager',
    'version': '17.0.1.0.1',
    'author': 'Ganemo',
    'website': 'https://www.ganemo.co',
    'summary':'This module helps to manage the attendance and/or absence of employees',
    'category': 'Payroll',
    'description': """
    Is a  module designed to manage employee attendance and absence, it is likely intended to facilitate tracking and managing work hours as well as scheduled or unplanned absences of employees.
    """,
    'depends': [
        'hr_attendance',
        'hr_holidays',
        'absence_day'
    ],
    'data': [
        'data/hr_leave_type_data.xml',
        'data/ir_cron_data.xml',
        'views/hr_attendance_views.xml',
        'views/hr_employee_views.xml',
        'views/hr_leave_views.xml',
        'views/hr_leave_type_views.xml',
    ],
    'installable': True,
    'auto_install': False,
    'license': 'Other proprietary',
    'currency': 'USD',
    'price': 20.0,
    'module_type': 'official'
}
