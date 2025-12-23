{
    'name': 'Formato 3.4 Libro de Inventarios y Balances - Cuentas por Cobrar al Personal: Trab. Soc. Acc. Ger. Direc.',
    'version': '17.0.1.0.1',
    'author': 'Ganemo',
    'website': 'https://www.ganemo.co',
    'category': 'Accounting',
    'live_test_url': 'https://www.ganemo.co/demo',
    'summary': 'This module creates the format 3.4 "Accounts receivable from workers" of the electronic inventory and balance book.',
    'description': """
This module creates the format 3.4 "Accounts receivable from workers" of the electronic inventory and balance book.
""",
    'depends': [
        'ple_sale_book',
        'financial_statement_annexes',
        'ple_inv_and_bal_0302',
    ],

    'data': [
        'security/ir.model.access.csv',
        'reports/ple_inv_bal_04_report.xml',
        'reports/ple_inv_bal_04_template.xml',
        'views/ple_report_inv_bal_one_views.xml',
        'views/ple_report_inv_bal_04_views.xml',
    ],
    'assets': {
        "web.report_assets_common": [
            "ple_inv_and_bal_0304/static/src/css/main.css",
        ],
    },
    'installable': True,
    'auto_install': False,
    'license': 'Other proprietary',
    'currency': 'USD',
    'price': 25.00,
    'module_type': 'official',
}
