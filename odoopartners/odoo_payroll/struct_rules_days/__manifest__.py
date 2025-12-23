{
    'name': 'Struct Rules Days',
    'version': '17.0.1.1.0',
    'author': 'Ganemo',
    'website': 'https://www.ganemo.co',
    'category': 'Human Resources/Payroll',
    'summary': '"Day Rules" tab in salary structures',
    'description': """
This module has been designed with the purpose of extending the configuration actions in the 
hr.payroll.structure model by adding a many2many type field called "Days Rules" (struct_days_ids). 

The objective is to filter the lines of the "Days worked and entries" by removing the lines defined 
in the struct_days_ids field at the time of executing the payroll.
""",
    'depends': [
        'hr_payroll'
    ],
    'data': [
        'views/hr_payroll_structure_views.xml'
    ],
    'application': False,
    'installable': True,
    'auto_install': False,
    'license': 'Other proprietary',
    'currency': 'USD',
    'price': 20.00
}
