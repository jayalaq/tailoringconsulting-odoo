{
    'name': 'Formato 3.13 Libro de Inventarios y Balances - Cuentas por Pagar diversas de Terceros y Relacionadas',
    'version': '17.0.1.0.0',
    'author': 'Ganemo',
    'website': 'https://www.ganemo.co',
    'category': 'Accounting',
    'summary': 'This module creates the format 3.13 Related Accounts Payable of the electronic inventory and balance book.',
    'description': """ 
This module enables the generation and workflow of the Accounting Report for Inventory and Balance Books, specifically for accounts payable to third parties and related entities. The reports can be exported in .txt, .xlsx, and .pdf formats, facilitating their presentation and compliance with accounting requirements for SUNAT.
""",
    'depends': [
        'ple_sale_book',
        'financial_statement_annexes',
        'ple_inv_and_bal_0302',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/ple_report_inv_bal_one_views.xml',
        'reports/ple_inv_bal_report.xml',
        'reports/ple_inv_bal_template.xml',
    ],
    'assets': {
        'web.report_assets_common': [
            'ple_inv_and_bal_0313/static/src/css/main.css',
        ]
    },
    'application': False,
    'installable': True,
    'auto_install': False,
    'license': 'Other proprietary',
    'currency': 'USD',
    'price': 25.00,
    'module_type': 'official',
}
