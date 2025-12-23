{
    'name': 'Payment Conditions',
    'version': '17.0.1.0.0',
    'author': 'Ganemo',
    'website': 'https://www.ganemo.co',
    'category': 'Human Resources/Payroll',
    'summary': 'This module creates recurrence fields in the contract and in the structure',
    'description': """
This model was created to manage payment conditions in commercial transactions. This module creates periodicity fields in the contract and in the structure.
""",
    'depends': [
        'localization_menu',
        'hr_payroll'
    ],
    'data': [
        'security/ir.model.access.csv',
        'data/payment_period_data.xml',
        'data/payment_type_data.xml',
        'data/special_situation_data.xml',
        'data/variable_payment_data.xml',
        'views/payment_period_menus.xml',
        'views/payment_type_menus.xml',
        'views/special_situation_menus.xml',
        'views/hr_contract_views.xml',
        'views/hr_payroll_structure_type_views.xml',
        'views/hr_payroll_structure_views.xml',
        'views/payment_period_views.xml',
        'views/payment_type_views.xml',
        'views/special_situation_views.xml',        
        'views/variable_payment_views.xml'
    ],
    'application': False,
    'installable': True,
    'auto_install': False,
    'license': 'Other proprietary',
    'currency': 'USD',
    'price': 20.0
}
