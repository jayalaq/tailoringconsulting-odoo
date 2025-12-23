{
    'name': 'Legal Data',
    'version': '17.0.1.1.0',
    'author': 'Ganemo',
    'live_test_url': 'https://www.ganemo.co/demo',
    'website': 'https://www.ganemo.co',
    'category': 'Payroll',
    'summary': 'Allows to create legal representative field in odoo.',
    'description': """
    This module was created in order to create a field called legal representative (legal_representative) and “Object” (object_company) model res.company in the settings / users and companies / companies module and in this way be able to collect relevant data about the company.
    """,
    'depends': [
        'base',
        'mail',
    ],
    'data': [
        'views/res_company_views.xml',
    ],
    'installable': True,
    'auto_install': False,
    'license': 'Other proprietary',
    'currency': 'USD',
    'price': 20.00
}
