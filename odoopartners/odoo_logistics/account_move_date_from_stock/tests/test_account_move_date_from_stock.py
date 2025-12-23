from odoo.tests import common

class TestAccountMoveDateFromStock(common.TransactionCase):
    def setUp(self):
        super(TestAccountMoveDateFromStock, self).setUp()

        self.product_category_obj = self.env['product.category']
        self.product_template_obj = self.env['product.template']
        self.res_partner_obj = self.env['res.partner']
        self.purchase_order_obj = self.env['purchase.order']
        self.stock_valuation_layer_obj = self.env['stock.valuation.layer']

    def test_stock_valuation_layer_effective_date(self):

        product_category = self.product_category_obj.create({
            'name': 'category test',
            'property_cost_method': 'average',
            'property_valuation': 'real_time',
        })
        product_template = self.product_template_obj.create({
            'name': 'Producto test',
            'default_code': 'product_test_1',
            'sale_ok': True,
            'purchase_ok': True,
            'type': 'product',
            'categ_id': product_category.id,
            'uom_id': self.env.ref('uom.product_uom_litre').id,
            'uom_po_id': self.env.ref('uom.product_uom_litre').id,
            'list_price': 20.0,
            'standard_price': 10.0
        })
        partner = self.res_partner_obj.create({
            'name': 'Ferretería Caviedes SA',
        })

        purchase_order = self.purchase_order_obj.create({
            'partner_id': partner.id,
            'order_line': [(0, 0, {
                'product_id': product_template.product_variant_id.id,
                'product_qty': 10,
                'price_unit': 10.0,
            })],
        })
        purchase_order.button_confirm()

        stock_picking = purchase_order.picking_ids
        stock_picking.button_validate()

        valuation_layer = self.stock_valuation_layer_obj.search([
            ('stock_move_id', 'in', stock_picking.move_line_ids_without_package.mapped('move_id').ids)
        ])

        self.assertEqual(stock_picking.date_done, valuation_layer.accounting_date,
                         "La fecha efectiva en la valoración de stock no coincide con la fecha contable después de validar")
