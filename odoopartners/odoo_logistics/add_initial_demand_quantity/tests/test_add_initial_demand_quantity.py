from odoo.tests import tagged, TransactionCase
from odoo import fields

@tagged('-at_install', 'post_install')
class TestMrpProductionActionConfirm(TransactionCase):

    def setUp(self):
        super().setUp()

        self.warehouse = self.env['stock.warehouse'].create({
            'name': 'Test Warehouse',
            'code': 'TWH',
        })

        self.uom_unit = self.env.ref('uom.product_uom_unit')

        self.finished_product = self.env['product.product'].create({
            'name': 'Finished Product',
            'type': 'product',
            'uom_id': self.uom_unit.id,
            'uom_po_id': self.uom_unit.id,
        })
        self.pre_production_loc = self.env['stock.location'].create({
            'name': 'Pre-Production',
            'usage': 'production',
        })

        self.post_production_loc = self.env['stock.location'].create({
            'name': 'Post-Production',
            'usage': 'production',
        })

        self.virtual_loc = self.env['stock.location'].create({
            'name': 'Virtual Location',
            'usage': 'production',
        })

        self.wh_simple_loc = self.env['stock.location'].create({
            'name': 'Simple Warehouse Location',
            'usage': 'internal',
        })
        self.raw_product = self.env['product.product'].create({
            'name': 'Raw Material',
            'type': 'product',
            'uom_id': self.uom_unit.id,
            'uom_po_id': self.uom_unit.id,
        })

        self.rule_1 = self.env['stock.rule'].create({
            'name': 'Rule 1 - Reabastecimiento',
            'route_id': self.warehouse.mto_pull_id.route_id.id,
            'location_src_id': self.wh_simple_loc.id,
            'location_dest_id': self.pre_production_loc.id,
            'picking_type_id': self.env['stock.picking.type'].search([], limit=1).id,
            'action': 'pull',
            'extra_pt': True,
        })

        self.rule_2 = self.env['stock.rule'].create({
            'name': 'Rule 2 - Movimiento Interno',
            'route_id': self.warehouse.mto_pull_id.route_id.id,
            'location_src_id': self.pre_production_loc.id,
            'location_dest_id': self.virtual_loc.id,
            'picking_type_id': self.env['stock.picking.type'].search([], limit=1).id,
            'action': 'pull',
            'extra_pt': True,
        })

        self.rule_3 = self.env['stock.rule'].create({
            'name': 'Rule 3 - Producción',
            'route_id': self.warehouse.mto_pull_id.route_id.id,
            'location_src_id': self.post_production_loc.id,
            'location_dest_id': self.wh_simple_loc.id,
            'picking_type_id': self.env['stock.picking.type'].search([], limit=1).id,
            'action': 'push',
            'extra_pt': True,
        })

        self.custom_route = self.env['stock.route'].create({
            'name': 'Fabricacion de 3 pasos',
            'warehouse_selectable': True,
            'sequence': 10,
            'rule_ids': [(6, 0, [self.rule_2.id, self.rule_2.id, self.rule_3.id])]
        })

        self.bom = self.env['mrp.bom'].create({
            'product_tmpl_id': self.finished_product.product_tmpl_id.id,
            'product_qty': 1.0,
            'type': 'normal',
            'bom_line_ids': [(0, 0, {
                'product_id': self.raw_product.id,
                'product_qty': 2.0,
            })]
        })

    def test_action_confirm_updates_initial_demand(self):
        huevo = self.env['product.product'].create({
            'name': 'Huevo',
            'type': 'product',
            'uom_id': self.env.ref('uom.product_uom_unit').id,
        })

        harina = self.env['product.product'].create({
            'name': 'Harina',
            'type': 'product',
            'uom_id': self.env.ref('uom.product_uom_kgm').id,
        })

        azucar = self.env['product.product'].create({
            'name': 'Azúcar',
            'type': 'product',
            'uom_id': self.env.ref('uom.product_uom_kgm').id,
        })

        production = self.env['mrp.production'].create({
            'product_id': self.finished_product.id,
            'bom_id': self.bom.id,
            'product_qty': 1.0,
            'location_src_id': self.warehouse.lot_stock_id.id,
            'location_dest_id': self.warehouse.lot_stock_id.id,
        })
        ingredients = [
            {'product': huevo, 'qty': 2.0},
            {'product': harina, 'qty': 1.5},
            {'product': azucar, 'qty': 1.0},
        ]

        moves = []
        for ingredient in ingredients:
            move = self.env['stock.move'].create({
                'name': f"Consumo de {ingredient['product'].name}",
                'product_id': ingredient['product'].id,
                'product_uom_qty': ingredient['qty'],
                'product_uom': ingredient['product'].uom_id.id,
                'location_id': self.warehouse.lot_stock_id.id,
                'location_dest_id': production.location_dest_id.id,
                'raw_material_production_id': production.id,
                'state': 'confirmed',
            })
            moves.append(move.id)

        production.write({'move_raw_ids': [(6, 0, moves)]})

        production.action_confirm()
        print('--------------------------------------------')
        print('Pickings generados:', production.picking_ids)
        print('--------------------------------------------')
