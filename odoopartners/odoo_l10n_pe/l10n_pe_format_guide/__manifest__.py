{
    'name': 'l10npe_formatguide',
    'version': '17.0.1.3.2',
    'author': 'Ganemo',
    'website': 'https://www.ganemo.co',
    'category': 'Accounting',
    "summary": "The object is to create a predefined format so that you can print under an already established template.",
    'description': """
The object is to create a predefined format so that you can print under an already established template.
""",    
    'depends': [
        'account', 
        'base', 
        'l10n_pe_edi_stock', 
        'l10n_latam_base', 
        'invoice_type_document_extension', 
        'l10n_pe_delivery_note_20_extension',
        'stock_barcode'
    ],
    'data': [
        'reports/stock_picking_report.xml',
        'reports/report_guide.xml',
        'views/res_partner_views.xml',
        'views/product_template_views.xml',
        'views/stock_picking_views.xml',
    ],
    'post_init_hook': '_trasnfer_data_to_horario_almacen',
    'license': 'Other proprietary',
    'currency': 'USD',
    "price": 00.00,
    'installable': True,
    'auto_install': False,
    'module_type': 'official'
}
