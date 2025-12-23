{
    'name': 'Automatic Leave Type',
    'version': '17.0.1.0.0',
    'author': 'Ganemo',
    'website': 'https://www.ganemo.co',
    'category': 'Human Resources/Payroll',
    'summary': 'Administration of Types of Absences in the Electronic Form of Peru',
    'description': """ 
This module imports the types of absences that exist in the Electronic Form of Peru. The main functionality of this module is to facilitate the process of incorporating and updating information related to employee absences.
""",
    'depends': [
        'hr_payroll',
        'project_timesheet_holidays',
        'hr_work_entry_holidays',
        'absence_manager'
    ],
    'data': [
        'data/hr_work_entry_type_data.xml',
        'data/hr_leave_type_data.xml',
        'views/hr_work_entry_type_views.xml'
    ],
    'application': False,
    'installable': True,
    'auto_install': False,
    'license': 'Other proprietary',
    'currency': 'USD',
    'price': 20.0
}
