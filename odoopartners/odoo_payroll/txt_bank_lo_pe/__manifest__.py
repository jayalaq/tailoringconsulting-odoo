{
    'name': 'txt_bank_lo_pe',
    'version': '17.0.1.0.5',
    'author': 'Ganemo',
    'website': 'https://www.ganemo.co',
    'category': 'Payroll',
    'summary': 'This module allows to issue txt files for the payment of the payroll',
    'description': """ 
This module has been designed with the purpose of allowing you to generate Txt from the banks BCP, BBVA, Interbank and Scotiabank to make payroll payments through telecredit.
""",
    'depends': [
        'hr_localization_menu',
        'type_bank_accounts',
        'hr_payroll',
        'financial_entity_sunat_code',
        'identification_type_employee',
        'personal_information'
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/hr_massive_payment_menus.xml',
        'views/hr_massive_payment_views.xml',
        'views/res_partner_bank_views.xml',
        'views/hr_payslip_views.xml',
    ],
    'application': False,
    'installable': True,
    'auto_install': False,
    'license': 'Other proprietary',
    'currency': 'USD',
    'price': 20.00,
    'module_type': 'official',
}
