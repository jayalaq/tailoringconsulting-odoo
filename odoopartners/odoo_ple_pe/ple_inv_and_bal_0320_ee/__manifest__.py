{
    'name': 'Formato 3.20 Libro de Inventarios y Balances - Estado de resultados (Enterprise)',
    'version': '17.0.1.0.0',
    'author': 'Ganemo',
    'website': 'https://www.ganemo.co',
    'summary': 'This module creates the format 3.20 "Statement of income" of the electronic inventory and balance book (Enterprise).',
    'description': 'This module creates the format 3.20 "Statement of income" of the electronic inventory and balance book (Enterprise).',
    'category': 'Accounting',
    'depends': [
        'account_reports',
        'ple_inv_and_bal_0301'
    ],
    'data': [
        'security/ir.model.access.csv',
        'reports/ir_actions_report.xml',
        'reports/ir_actions_report_templates.xml',
        'views/account_report_views.xml',
        'wizards/wizard_report_txt_ple_3_20_views.xml',        
    ],
    'installable': True,
    'auto_install': False,
    'license': 'Other proprietary',
    'currency': 'USD',
    'price': 50.00,
    'module_type': 'official'
}
