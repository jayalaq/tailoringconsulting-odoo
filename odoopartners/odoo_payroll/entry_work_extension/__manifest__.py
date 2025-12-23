{
    'name': 'Entry work extension',
    'version': '17.0.1.0.0',
    'author': 'Ganemo',
    'website': 'https://www.ganemo.co',
    'category': 'Payroll',
    'summary':'Management of loans and salary advances to employees',
    'description': """  
Payroll Advance Policy The Payroll Advance Policy describes the terms for providing salary advances to our employees as a short-term emergency loan.
""",
    'depends': [
        'hr_payroll', 
        'hr_work_entry_contract'
    ],
    'data': [
        'wizards/hr_work_entry_regeneration_wizard_views.xml',
    ],
    'application': False,
    'installable': True,
    'auto_install': False,
    'license': 'Other proprietary',
    'currency': 'USD',
    'price': 20.00,
    'module_type': 'official',
}
