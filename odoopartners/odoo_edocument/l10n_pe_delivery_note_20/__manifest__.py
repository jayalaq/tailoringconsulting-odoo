{
    'name': 'Peruvian - Electronic Delivery Note extension',
    'version': '17.0.1.0.5',
    'author': 'Ganemo',
    'license': 'Other proprietary',
    'website': 'https://www.ganemo.co',
    'summary': 'extend Odoo native functions for electronic waybill - sender',
    'description': """
The scope of this module is to improve functionalities of the Electronic Referral Guide - Sender.
    """,
    'live_test_url': 'https://www.ganemo.co/demo',
    'category': 'Accounting',
    'depends': [
        'l10n_pe_edi_stock',
        'l10n_pe_delivery_note_ple',
        'third_parties_delivery',
        'tributary_address_extension'
    ],
    'data': [
        'data/edi_delivery_guide.xml',
        'views/stock_picking_views.xml',
        'views/stock_picking_views_button.xml',
        'views/report_deliveryslip.xml',
        'views/res_config_settings_views.xml'
    ],
    'currency': 'USD',
    'module_type': 'official',
    'price': 150.00
}
