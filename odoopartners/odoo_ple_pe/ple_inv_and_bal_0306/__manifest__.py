{
    'name': 'Formato 3.6 Libro de Inventarios y Balances - Estimación de cuentas de cobranza dudosa',
    'version': '17.0.1.0.0',
    'author': 'Ganemo',
    'website': 'https://www.ganemo.co',
    'summary': 'This module creates the format 3.6 "estimate of doubtful accounts receivable" of the electronic inventory and balance book.',
    'category': 'Accounting',
    'depends': [
        'ple_permanent_inventory_in_physical_units',
        'ple_inv_and_bal_0301',
        'ple_inv_and_bal_0302',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/account_move_views_inherit.xml',
        'views/ple_inv_bal_views_02_inherit.xml',
        'reports/ple_inv_bal_06_report.xml',
        'reports/ple_inv_bal_06_template.xml',
    ],
    'installable': True,
    'auto_install': False,
    'license': 'Other proprietary',
    'currency': 'USD',
    'module_type': 'official',
    'price': 35.00
}
