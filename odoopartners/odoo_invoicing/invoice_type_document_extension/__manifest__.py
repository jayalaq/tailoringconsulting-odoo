{
    "name": "Related fields for purchases and sales",
    "version": "17.0.1.0.0",
    "author": "Ganemo",
    "website": "https://www.ganemo.co",
    'category': 'Accounting',
    "summary": "This module will allow us to place the type of document, document series and payment voucher number automatically through the records of purchase and sale invoices.",
    "description": """This module will allow us to place the type of document, document series and payment voucher number automatically through the records of purchase and sale invoices.""",
    "depends": [
        'invoice_type_document', 
        'stock', 
        'l10n_pe_delivery_note_ple',
        'purchase_stock',
        'sale_stock'
    ],
    'data': [
        'views/stock_picking_views.xml'
    ],
    'application': False,
    "installable": True,
    "auto_install": False,
    "license": "Other proprietary",
    "currency": "USD",
    "price": 20.00,
    'module_type': 'official'
}
