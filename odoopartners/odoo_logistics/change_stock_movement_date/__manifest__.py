{
    'name': 'Change stock movement date',
    'version': '17.0.1.0.1',
    'author': 'Ganemo',
    'website': 'https://www.ganemo.co',
    'live_test_url': 'https://www.ganemo.co',
    'category': 'Warehouse',
    'summary': 'It allows you to enter an "effective date" of the transfer that will be taken to register the delivery voucher, instead of the date when it is validated. Without this module, Odoo always takes the validation date. It also creates the "accounting date" field in the "Stock Movements" and in the "Product Movements',
    'description': """
Allows you to enter an "effective date" of the transfer that will be used to record the proof of delivery, instead of the date on which it is validated. Without this module, Odoo always takes the validation date. It also creates the "accounting date" field in the "Stock Movements" and in the "Product Movements".
The “Effective Date” field is a native Odoo field, now what this module will do is make this “Effective Date” field visible with the technical name “date_note” in the “stock.picking” model.
    """,
    'depends': ['stock'],
    'data': [
        'views/stock_picking_views.xml'
    ],
    'installable': True,
    'active': False,
    'license': 'Other proprietary',
    'currency': 'USD',
    'module_type': 'official',
    'price': 20.00
}
