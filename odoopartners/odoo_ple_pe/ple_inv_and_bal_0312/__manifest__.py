{
    'name': 'Formato 3.12 Libro de Inventarios y Balances - Cuentas por Pagar Comerciales de Terceros y Relacionadas',
    'version': '17.0.1.0.0',
    'author': 'Ganemo',
    'website': 'https://www.ganemo.co',
    'category': 'Accounting',
    'summary': 'This module creates the format 3.12 trade payables of the electronic inventory and balance book.',
    'description': """ 
This module enables the generation and flow of the Accounting Book of Inventories and Balances report, specifically for accounts payable to third parties and related parties, corresponding to accounts 42 and 43. The report is designed to meet SUNAT requirements and can be exported in .txt, .xlsx, and .pdf formats for submission.
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
    'application': False,
    'installable': True,
    'auto_install': False,
    'license': 'Other proprietary',
    'currency': 'USD',
    'price': 25.00,
    'module_type': 'official',
}
