{
    'name': 'Automatic functions rule',
    'version': '17.0.1.0.1',
    'author': 'Ganemo',
    'website': 'https://www.ganemo.co',
    'category': 'Payroll',
    'summary': ' Validates in the "Payroll calculation" tab of the hr.payslip, the salary rules that have an amount equal to "0.00" and eliminates them',
    'description': """
Validate in the “Payroll calculation” tab of hr.payslip, the salary rules that have an amount equal to “0.00” (after having made your calculations) and delete them.

Add the following functionality to the “Calculate Sheet” button of the hr.payslip of the payslip module.

It will validate in the “Days worked and entries” tab of the hr.payslip, the entries (hr.payslip.input) that have an amount equal to “0.00” (after having made its validations) and will delete them.
Create a button called: “Eliminate Zeros"; which when pressed activates the functions described above, this to have manual operation support if at any time it is required.

The other function of this module is to reflect in the employee's salary receipt the concepts of other entries configured in the salary structure used
""",
    'depends': [
        'hr_payroll'
    ],
    'data': [
        'views/hr_payslip.xml',
    ],
    'installable': True,
    'auto_install': False,
    'license': 'Other proprietary',
    'currency': 'USD',
    'price': 20.00,
    'module_type': 'official',
}