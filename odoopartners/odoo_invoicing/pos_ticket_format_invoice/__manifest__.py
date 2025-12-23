{
    'name': 'Pos Ticket Format Invoice',
    'version': '17.0.2.1.0',
    'author': 'Ganemo',
    'website': 'https://www.ganemo.co/',
    'category': 'Accounting/Point of Sale',
    'summary': 'Add an additional format to invoices POS ticket type which allows the use of thermal printers',
    'description': """
This module creates a new Ticket Type Format to use in printing the Invoice, in this way thermal printers can be used to print the receipts.
""",
    'depends': [
        'account',
        'l10n_latam_invoice_document',
        'print_aditional_comment',
        'amount_to_text',
        'base_address_extended',
    ],
    'data': [
        'reports/invoice_ticket_report.xml',
        'reports/invoice_ticket_templates.xml',
        'views/account_journal_views.xml'
    ],
    'assets': {
        'web.report_assets_common': [
            'pos_ticket_format_invoice/static/src/css/main.css',
        ],
    },
    'application': False,
    'installable': True,
    'auto_install': False,
    'license': 'Other proprietary',
    'currency': 'USD',
    'price': 45.00
}
