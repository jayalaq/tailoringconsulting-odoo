{
    'name': 'Register of Cash and banks PLE - SUNAT (Perú)',
    'version': '17.0.1.0.0',
    'author': 'Ganemo',
    'website': 'https://www.ganemo.co/ple',
    'summary': 'Register of Cash and banks PLE - SUNAT (Perú).',
    'description': """
    Generates the electronic register of Cash and Banks in .txt file, ready to present to SUNAT via electronic book program (PLE - SUNAT).
    This is a mandatory e-book for companies that are required to keep complete accounting.
    """,
    'category': 'Accounting',
    'depends': [
        'ple_purchase_book',
        'l10n_pe_catalog',
        'financial_entity_sunat_code',
        'invoice_type_document'
    ],
    'data': [
        'data/rest_bank.xml',
        'views/account_views.xml',
        'views/ple_cash_book_views.xml',
        'security/ir.model.access.csv',
        'sql/data_structured_cash.sql',
        'sql/find_full_reconcile.sql',
        'sql/get_unit_operation_code.sql',
        'sql/UDF_numeric_char.sql'
    ],
    'application': False,
    'installable': True,
    'auto_install': False,
    'module_type': 'official',
    'license': 'Other proprietary',
    'currency': 'USD',
    'price': 160.00
}
