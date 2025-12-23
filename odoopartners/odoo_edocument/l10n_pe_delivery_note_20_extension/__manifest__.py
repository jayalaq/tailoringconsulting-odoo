{
    'name': 'Peruvian - Electronic Delivery Note extension 2',
    'version': '17.0.1.0.0',
    'author': 'Ganemo',
    'website': 'https://www.ganemo.co',
    'category': 'Accounting',
    'summary': 'Extend Odoo native functions for electronic waybill - sender',
    'description': """
Extend Odoo native functions for electronic waybill - sender.
""",
    'depends': [
        'l10n_pe_delivery_note_20',
        'localization_menu'
    ],
    'data': [
        'security/ir.model.access.csv',
        'data/edi_delivery_guide.xml',
        'data/port_catalog_data.xml',
        'data/airport_catalog_data.xml',
        'data/identification_code_tax_concept_data.xml',
        'views/stock_picking_views.xml',
        'views/port_catalog_views.xml',
        'views/airport_catalog_views.xml',
        'views/tariff_subheading_views.xml',
        'views/identification_code_tax_concept_views.xml',
        'views/product_template_views.xml'
    ],
    'application': False,
    'installable': True,
    'auto_install': False,
    'license': 'Other proprietary',
    'currency': 'USD',
    'price': 150.00,
    'module_type': 'official'
}
