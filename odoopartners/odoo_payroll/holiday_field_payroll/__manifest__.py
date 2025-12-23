{
    'name': 'Holiday field payroll',
    'version': '17.0.1.0.0',
    'author': 'Ganemo',
    'website': 'https://www.ganemo.co',
    'summary': 'Create the group of basic rules necessary for the calculation of regular payroll',
    'description': '''
    Regular payroll calculation requires the monthly salary, which is the total salary stipulated in 
    the employee's contract; the daily rate, calculated by dividing the monthly salary by the number 
    of working days in the month; and the hourly rate, determined by dividing the daily rate by the 
    standard number of work hours per day. Standard working hours must be defined, and any hours worked 
    beyond these are considered overtime and are usually compensated at a higher rate.
''',
    'live_test_url': 'https://www.ganemo.co/demo',
    'depends': ['holiday_process'],
    'data': ['views/hr_payslip_views.xml'],
    'installable': True,
    'auto_install': False,
    'license': 'Other proprietary',
    'currency': 'USD',
    'price': 0.00
}
