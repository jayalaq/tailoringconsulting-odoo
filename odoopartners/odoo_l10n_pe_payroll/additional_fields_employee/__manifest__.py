{
    'name': 'Additional Fields Employee',
    'version': '17.0.1.0.0',
    'author': 'Ganemo',
    'website': 'https://www.ganemo.co',
    'category': 'Human Resources/Payroll',
    'summary': 'Field Management in Employee Records and Contracts',
    'description': """
This module has been created with the purpose of improving the management of employees' personal information by allowing the assignment of the health, disability and work status regime that corresponds to them, with the aim of offering greater flexibility in data collection.

This module introduces the following fields into the model employee file 'hr.employee':

- health_regime_id: It will be of type Many2one where a relationship with all the health regimens registered in the 'health.regime' model is displayed.
- disability: It will be of type Boolean.

In the employee contract, model 'hr.contract' creates the following fields:

- labor_regime_id
- labor_condition_id
- work_occupation_id
- maximum_working_day
- atypical_cumulative_day
- nocturnal_schedule
- unionized
- is_practitioner
""",
    'depends': [
        'hr_contract',
        'localization_menu'
    ],
    'data': [
        'security/ir.model.access.csv',
        'data/academic_degree_data.xml',
        'data/health_regime_data.xml',
        'data/type_contract_data.xml',
        'data/work.occupation.csv',
        'views/academic_degree_menus.xml',
        'views/academic_degree_views.xml',
        'views/employee_regime_menus.xml',
        'views/employee_regime_views.xml',
        'views/health_regime_menus.xml',
        'views/health_regime_views.xml',
        'views/hr_contract_views.xml',
        'views/hr_employee_views.xml',
        'views/type_contract_menus.xml',
        'views/type_contract_views.xml',
        'views/work_occupation_menus.xml',
        'views/work_occupation_views.xml'
    ],
    'application': False,
    'installable': True,
    'auto_install': False,
    'license': 'Other proprietary',
    'currency': 'USD',
    'price': 20.00
}
