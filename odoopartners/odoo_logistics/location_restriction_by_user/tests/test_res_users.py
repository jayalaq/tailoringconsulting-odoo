# test_stock_picking.py
from odoo.tests import common
from odoo.exceptions import UserError


class TestStockPicking(common.TransactionCase):

    def setUp(self):
        super().setUp()
        self.warehouse = self.env['stock.warehouse'].create({
            'name': 'Lima',
            'code': 'Li',
            'active': True,
            'user_ids': [self.env.user.id]
        })

        self.location = self.env['stock.location'].create({
            'name': 'Li/Stock',
            'usage': 'internal',
            'user_ids_01': [self.env.user.id],
            'user_ids_02': [self.env.user.id]
        })

        self.picking_type = self.env['stock.picking.type'].create({
            'name': 'Picking de Prueba',
            'code': 'internal',
            'sequence_code': 'INT',
            'default_location_src_id': self.location.id,
            'default_location_dest_id': self.location.id
        })

        self.product = self.env['product.product'].create({
        'name': 'Producto de Prueba',
        'type': 'product',
        })

    def test_compute_location_id(self):
        """
        Prueba el método _compute_location_id
        """
        picking = self.env['stock.picking'].create({
            'picking_type_id': self.picking_type.id,
            'partner_id': False,
        })

        picking._compute_location_id()
        self.assertEqual(picking.location_id, self.picking_type.default_location_src_id)

    def test_button_validate_allowed(self):
        """
        Prueba el método button_validate cuando el usuario esta asignado como responsable en 'stock.location'
        """
        other_location = self.env['stock.location'].create({
            'name': 'Li/Stock2',
            'usage': 'internal',
            'user_ids_02':[self.env.user.id]
        })

        picking = self.env['stock.picking'].create({
            'picking_type_id': self.picking_type.id,
            'location_id': self.location.id,
            'location_dest_id': other_location.id,
        })

        move = self.env['stock.move'].create({
            'name': 'Movimiento de Prueba',
            'product_id': self.product.id,
            'product_uom_qty': 1,
            'product_uom': self.product.uom_id.id,
            'picking_id': picking.id,
            'location_id': self.location.id,
            'location_dest_id': other_location .id,
            })
        
        picking.button_validate()
        self.assertEqual(picking.state, 'done')


    def test_button_validate_not_allowed(self):
        """
        Prueba el método button_validate cuando el usuario no este asignado como responsable en 'stock.location'
        """
        other_user = self.env['res.users'].create({
            'name': 'Otro Usuario',
            'login': 'otrousuario',
        })

        other_location = self.env['stock.location'].create({
            'name': 'Li/Stock3',
            'usage': 'internal',
            'user_ids_02': [other_user.id]
        })

        picking = self.env['stock.picking'].create({
            'picking_type_id': self.picking_type.id,
            'location_id': self.location.id,
            'location_dest_id': other_location.id,
        })

        move = self.env['stock.move'].create({
            'name': 'Movimiento de Prueba 2',
            'product_id': self.product.id,
            'product_uom_qty': 1,
            'product_uom': self.product.uom_id.id,
            'picking_id': picking.id,
            'location_id': self.location.id,
            'location_dest_id': other_location.id,
            })

        with self.assertRaises(UserError):
            picking.button_validate()
