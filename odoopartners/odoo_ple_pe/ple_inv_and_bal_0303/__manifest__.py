{
    'name': 'Formato 3.3 Libro de Inventarios y Balances - Cuentas por Cobrar Comerciales de Terceros y Relacionadas',
    'version': '17.0.1.0.0',
    'author': 'Ganemo',
    'website': 'https://www.ganemo.co',
    'category': 'Accounting',
    'summary': 'Accounts Receivable Format 3.3 for Electronic Inventory and Balance Book',
    'description':""" 
This module creates the format 3.3 'accounts receivable' of the electronic inventory and balance book.
""",
    'depends': [
        'ple_sale_book',
        'financial_statement_annexes',
        'ple_inv_and_bal_0302',
    ],
    'data': [
        'security/ir.model.access.csv',
        'reports/ple_inv_bal_03_report.xml',
        'reports/ple_inv_bal_03_template.xml',
        'views/ple_report_inv_bal_one_views.xml',
        'views/ple_report_inv_bal_03_views.xml'
    ],
    'assets': {
        "web.report_assets_common": [
            "ple_inv_and_bal_0303/static/src/css/main.css",
        ],
    },
    'application': False,
    'installable': True,
    'auto_install': False,
    'license': 'Other proprietary',
    'currency': 'USD',
    'price': 25.00,
    'module_type': 'official'
}
