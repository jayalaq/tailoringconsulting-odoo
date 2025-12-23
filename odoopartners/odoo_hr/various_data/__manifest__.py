{
    'name': 'Various Data',
    'version': '17.0.1.1.1',
    'author': 'Ganemo',
    'website': 'https://www.ganemo.co',
    'category': 'Payroll',
    'summary': 'Creates the tax data menu in location, where the models of Minimum Vital Remuneration, UIT, SIS, SCTR are created',
    'description': """
    This module provides functionalities for the creation, updating, and monitoring of specific models related to Minimum Vital Remuneration, Unidad Impositiva Tributaria(UIT), Seguro Integral de Salud (SIS), and Seguro Complementario de Trabajo de Riesgo (SCTR).
    """,
    'depends': [
        'localization_menu',
        'hr',
        'eps_process'
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/hr_employee_views.xml',
        'views/various_data_rmv_views.xml',
        'views/various_data_sctr_views.xml',
        'views/various_data_sis_views.xml',
        'views/various_data_uit_views.xml'
    ],
    'application': False,
    'installable': True,
    'auto_install': False,
    'license': 'Other proprietary',
    'currency': 'USD',
    'price': 20.0
}
