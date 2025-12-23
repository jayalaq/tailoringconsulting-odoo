{
    'name': 'HR Localization Menu',
    'version': '17.0.1.1.0',
    'author': 'Ganemo',
    'website': 'https://www.ganemo.co',
    'category': 'Human Resources/Payroll',
    'summary': 'Creates localization menu for payroll',
    'description': """
This module creates the parent menu localization in the payroll menu.    
""",
    'depends': [
        'hr_payroll'
    ],
    'data': [
        'views/l10n_pe_hr_menus.xml'
    ],
    'application': False,
    'installable': True,
    'auto_install': False,
    'license': 'Other proprietary',
    'currency': 'USD',
    'price': 5.00
}
