{
    'name': 'Edit Days',
    'version': '17.0.1.0.0',
    'author': 'Ganemo',
    'website': 'https://www.ganemo.co',
    'category': 'Payroll',
    'summary': 'Allow editing in the monthly payroll before calculating the sheet in "days worked and entries" the number of days, amount and number of hours in the payslip.',
    'description': """
    This module was created with the objective of being able to edit in the Payroll module, in the payroll and in the tab “days worked and entries” model (hr.payslip.worked_days) the numbers of days (number_of_days), hours (number_of_hours) and the amount (aumont).
    """,
    'depends': [
        'hr_payroll'
    ],
    'data': [
        'views/hr_payslip_views.xml',
    ],
    'installable': True,
    'auto_install': False,
    'license': 'Other proprietary',
    'currency': 'USD',
    'price': 20.00
}
