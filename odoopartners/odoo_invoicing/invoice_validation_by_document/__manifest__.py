{
    'name': 'Invoice Validation by Document',
    'version': '17.0.1.0.1',
    'author': 'Ganemo',
    'website': 'https://www.ganemo.co',
    'category': 'Accounting/Accounting',
    'summary': 'This module will allow you to select and restrict the type of document and the payment receipts that the country has.',
    'description': """
This module will allow you to select and restrict the type of document and the payment receipts that the country has.
Only sale and purchase types of journals will be allow to be restricted.
    """,
    'depends': [
        'document_type_validation',
        'l10n_latam_invoice_document',
        'contacts'
    ],
    'data': [
        'views/invoice_validation_document.xml'
    ],
    'application': False,
    'installable': True,
    'auto_install': False,
    'license': 'Other proprietary',
    'currency': 'USD',
    'price': 50.00,
    'module_type': 'official', 
}