{
    'name': 'Automatic timesheets',
    'version': '17.0.1.0.0',
    'author': 'Ganemo',
    'website': 'https://www.ganemo.co',
    'category': 'Payroll Localization',
    'summary': 'Create the automatic overtime calculation function.',
    'description': '''
This module is useful for creating timesheets automatically based on 
attendance. Sometimes in some cases we need to create a timesheet 
automatically when an employee is unable to fill the timesheet 
like workers or office staff. Allows an employee to automatically
populate their timesheet based on their attendance. You must define 
the project and task in the timesheet settings for common use; 
You can also be assigned a project or task within the employee 
if you want to create a timesheet for an employee in other projects
 which are also possible with this option.
''',
    'depends': ['hr_timesheet'],
    'data': ['views/account_analytic_line_views.xml'],
    'installable': True,
    'auto_install': False,
    'application': False,
    'license': 'Other proprietary',
    'currency': 'USD',
    'price': 20.0
}
