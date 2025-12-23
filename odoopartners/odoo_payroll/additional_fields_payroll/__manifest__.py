{
    'name': 'Additional fields payroll',
    'version': '17.0.1.2.1',
    'author': 'Ganemo',
    'website': 'https://www.ganemo.co',
    'category': 'Payroll',
    'summary': 'Allows allocation of employee pension system',
    'description': """
Creates the fields for "Reason for Leaving", "Contract Type" and "In-kind Remuneration" in the pension system and enable the 
creation of icons for "Reason for Leaving", "Contract Type" and "In-kind Remuneration" in the employee/contract module.
    
This module allows the allocation of the employee's pension system.
Allows you to create in the employee / contract module the icons for the reason for leaving the type of contract and remuneration in kind.
""",
    'depends': [
        'localization_menu',
        'hr_payroll'
    ],
    'data': [
        'data/low_reason_data.xml',
        'security/ir.model.access.csv',
        'views/hr_views.xml',
        'views/low_reason_views.xml',
        'views/mintra_contract_views.xml'
    ],
    'installable': True,
    'auto_install': False,
    'application': False,
    'license': 'Other proprietary',
    'currency': 'USD',
    'price': 20.00
}
