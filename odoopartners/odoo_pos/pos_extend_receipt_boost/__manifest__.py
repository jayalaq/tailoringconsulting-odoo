{
    "name": "Advance POS Receipt Boost",
    "author": "Ganemo",
    "version": "17.0.1.0.1",
    "price": 50.00,
    "currency": "USD",
    "module_type": "official",
    "website": "https://www.ganemo.co",
    "summary": "Advance POS Receipt Boost",
    "description": """
This app help to add customer details, invoice number and barcode in pos receipt.
    """,
    "license": "Other proprietary",
    "depends": ["pos_ticket_base_template"],
    'assets': {
        'point_of_sale._assets_pos': [
            'pos_extend_receipt_boost/static/src/**/*',
        ],
    },
    "data": [
        "views/res_config_settings_views.xml",
    ],
    "auto_install": False,
    "installable": True,
    "category": "Point of Sale",
}
