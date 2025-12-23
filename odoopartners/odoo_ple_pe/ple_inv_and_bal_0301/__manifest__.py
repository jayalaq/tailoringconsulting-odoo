{
    'name': 'Formato 3.1 Libro de Inventarios y Balances - Estado de Situación Financiera',
    'version': '17.0.1.1.0',
    'author': 'Ganemo',
    'website': 'https://www.ganemo.co',
    'category': 'Accounting',
    'summary': 'Financial Position Statement Generator for Electronic Inventory (Format 3.1)',
    'description': """ 
This module creates the format 3.1 "Statement of financial position" of the electronic inventory and balance book.
""",
    'depends': [
        'ple_sale_book', 
        'l10n_pe_catalog',
        'ple_cash_book',
    ],
    'data': [
        'security/ir.model.access.csv',
        'data/tags_autolink.xml',
        'reports/ple_inv_bal_report.xml',
        'reports/ple_inv_bal_template.xml',
        'views/account_account_views.xml',
        'views/account_move_line_views.xml',
        'views/account_move_views.xml',
        'views/eeff_ple_menus.xml',
        'views/eeff_ple_views.xml',
        'views/ple_inv_bal_initial_balances_views.xml',
        'views/ple_report_inv_bal_menus.xml',
        'views/ple_report_inv_bal_views.xml',
        'sql/eeff_ple.sql',
    ],
    'application': False,
    'installable': True,
    'auto_install': False,
    'license': 'Other proprietary',
    'currency': 'USD',
    'price': 35.00,
    'module_type': 'official'
}
