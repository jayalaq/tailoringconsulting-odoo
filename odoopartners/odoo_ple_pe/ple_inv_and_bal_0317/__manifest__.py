{
    'name': 'Formato 3.17 Libro de Inventarios y Balances - Balance de Comprobación',
    'version': '17.0.1.0.0',
    'author': 'Ganemo',
    'website': 'https://www.ganemo.co',
    'category': 'Accounting',
    'summary': 'This module creates the format 3.17 of the electronic inventory and balance book.',
    'description': """
This module contains the generation and flow of the inventory and balance sheet accounting report - Trial Balance txt, xlsx and pdf.
""",
    'depends': [
        'ple_sale_book',
        'l10n_pe_catalog'
    ],
    'data': [
        'security/ir.model.access.csv',
        'data/trial_balances_codes.xml',
        'data/account_journal.xml',
        'reports/ple_inv_bal_seventeen_report.xml',
        'reports/ple_inv_bal_seventeen_template.xml',
        'views/ple_addition_deduction_views.xml',
        'views/ple_initial_balances_seveenten_views.xml',
        'views/ple_report_inv_bal_seventeen_menus.xml',
        'views/ple_report_inv_bal_seventeen_views.xml',
        'views/ple_transfers_cancellations_views.xml',
        'views/trial_balance_catalog_menus.xml',
        'views/trial_balance_catalog_views.xml',
        'views/account_account_views.xml',
    ],
    'application': False,
    'installable': True,
    'auto_install': False,
    'post_init_hook': '_update_data_trial_balances',
    'license': 'Other proprietary',
    'currency': 'USD',
    'price': 50.00,
    'module_type': 'official'
}
