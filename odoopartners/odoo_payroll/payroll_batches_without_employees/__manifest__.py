{
    'name': 'Payroll batches without employees',
    'version': '17.0.1.0.0',
    'author': 'Ganemo',
    'website': 'https://www.ganemo.co',
    'category': 'Human Resources/Payroll',
    'summary': 'Create a button that allows you to delete the employees that are pre-loaded in the "Wizard" for the payroll run from the Payroll Batches',
    'description': """
This module, "payroll_batches_without_employees," adds a button that allows users to remove pre-loaded employees from the payroll run wizard within Payroll Batches. It is designed to streamline the payroll process by providing a simple solution to exclude specific employees from batch payroll runs, ensuring that only the relevant employee records are processed. This module supports both enterprise and community versions of Odoo, making it versatile and widely applicable. It integrates seamlessly with the existing hr_payroll module and enhances the user experience by offering greater control over payroll batch management.
    """,
    'depends': ['hr_payroll'],
    'data': [
        'views/hr_payslip_employees_views.xml',
    ],
    'installable': True,
    'auto_install': False,
    'license': 'Other proprietary',
    'currency': 'USD',
    'price': 20.0,
    'module_type': 'official',
}
