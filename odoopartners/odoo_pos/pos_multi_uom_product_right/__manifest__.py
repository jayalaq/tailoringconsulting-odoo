{
    "name": "POS multi UOM product right",
    "version": "17.0.1.0.1",
    "author": "Ganemo",
    "website": "https://www.ganemo.co/",
    "summary": "This module allows you to modify the unit of measure used in the sale of products at the point of sale.",
    "description": """
    This module allows you to modify the unit of measure used in the sale of products at the point of sale.
    """,
    "category": "Point of Sale",
    "depends": ["point_of_sale"],
    "data": [
        "views/pos.xml",
        "views/product.xml",
    ],
    "assets": {
        "point_of_sale._assets_pos": [
            "pos_multi_uom_product_right/static/src/**/*",
        ],
    },
    "installable": True,
    "auto_install": False,
    "license": "Other proprietary",
    "currency": "USD",
    "module_type": "official",
    "price": 40.00,
}
