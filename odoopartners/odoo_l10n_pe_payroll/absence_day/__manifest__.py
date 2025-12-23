{
    'name': 'Absence day',
    'version': '17.0.1.0.0',
    'author': 'Ganemo',
    'website': 'https://www.ganemo.co',
    'category': 'Payroll',
    'summary': 'Modifies the absence module',
    'description': """
    This module modifies in the absence module, the Days count between the From field and the To field,
    taking into account the days that the worker does not provide service.
    """,
    'depends': ['hr_payroll'],
    'data': [
        'security/ir.model.access.csv',
        'data/ir_cron.xml',
        'data/hr_work_entry_type_data.xml',
        'views/resource_views.xml',
        'views/wizard_views.xml'
    ],
    'installable': True,
    'auto_install': False,
    'application': False,
    'license': 'Other proprietary',
    'currency': 'USD',
    'price': 20.0
}
