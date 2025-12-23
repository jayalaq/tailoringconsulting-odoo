{
    'name': 'Document in Supplier Invoice',
    'version': '17.0.1.0.1',
    'author': 'Ganemo',
    'website': 'https://www.ganemo.co',
    'category': 'Accounting/Accounting',
    'summary': "For each type of document, you can decide whether it will be used for the supplier invoice record...",
    'description': """
Configure in each type of document, the purchase journal and the sale journal with which this type of document can be used. So we
can use documents type's in supplier invoices and supplier corrective invoices. It is very useful for countries where different types 
of tax documents are distinguished, as is the case in many Latin American countries.
""",
    'depends': [
        'account',
        'l10n_latam_invoice_document',
        'l10n_country_filter',
    ],
    'data': [
        'views/account_move.xml',
        'views/l10n_latam_identification_type.xml',
    ],
    'application': False,
    'installable': True,
    'auto_install': False,
    'license': 'Other proprietary',
    'currency': 'USD',
    'price': 20.00,
}