from odoo.tests import TransactionCase, tagged
from odoo.exceptions import ValidationError


@tagged('post_install', '-at_install')
class TestStockLotStatus(TransactionCase):

    def setUp(self):
        super().setUp()
        # Create basic records needed for testing
        self.product = self.env['product.product'].create({
            'name': 'Test Product',
            'type': 'product',
            'tracking': 'serial',
        })
        
        self.status_1 = self.env['stock.production.lot.status'].create({
            'code': 'NEW',
            'name': 'New Product'
        })
        
        self.status_2 = self.env['stock.production.lot.status'].create({
            'code': 'USED',
            'name': 'Used Product'
        })
        
        self.lot = self.env['stock.lot'].create({
            'name': 'TEST/001',
            'product_id': self.product.id,
            'company_id': self.env.company.id,
            'status': self.status_1.id,
        })

        # Create warehouse and locations
        self.warehouse = self.env['stock.warehouse'].search([], limit=1)
        self.stock_location = self.warehouse.lot_stock_id
        self.customer_location = self.env.ref('stock.stock_location_customers')

    def test_01_lot_status_creation(self):
        """Test creation of lot with status"""
        self.assertEqual(self.lot.status.id, self.status_1.id)
        self.assertEqual(self.lot.status.code, 'NEW')

    def test_02_move_line_status_compute(self):
        """Test compute status in move lines"""
        move = self.env['stock.move'].create({
            'name': 'Test Move',
            'product_id': self.product.id,
            'product_uom': self.product.uom_id.id,
            'product_uom_qty': 1,
            'location_id': self.stock_location.id,
            'location_dest_id': self.customer_location.id,
        })
        
        move_line = self.env['stock.move.line'].create({
            'move_id': move.id,
            'product_id': self.product.id,
            'product_uom_id': self.product.uom_id.id,
            'lot_id': self.lot.id,
            'location_id': self.stock_location.id,
            'location_dest_id': self.customer_location.id,
        })
        
        self.assertEqual(move_line.status.id, self.status_1.id)

    def test_03_picking_validation_status_update(self):
        """Test status update on picking validation"""
        picking = self.env['stock.picking'].create({
            'picking_type_id': self.warehouse.out_type_id.id,
            'location_id': self.stock_location.id,
            'location_dest_id': self.customer_location.id,
        })
        
        move = self.env['stock.move'].create({
            'name': 'Test Move',
            'product_id': self.product.id,
            'product_uom': self.product.uom_id.id,
            'product_uom_qty': 1,
            'picking_id': picking.id,
            'location_id': self.stock_location.id,
            'location_dest_id': self.customer_location.id,
        })
        picking.action_assign()
        move_line = self.env['stock.move.line'].create({
            'move_id': move.id,
            'product_id': self.product.id,
            'product_uom_id': self.product.uom_id.id,
            'lot_id': self.lot.id,
            'quantity': 1,
            'location_id': self.stock_location.id,
            'location_dest_id': self.customer_location.id,
            'status': self.status_2.id,
        })
        
        picking.button_validate()
        self.assertEqual(self.lot.status.id, self.status_1.id)

    def test_04_production_lot_status_name_search(self):
        """Test name_search method of production lot status"""
        # Test search by code
        result = self.env['stock.production.lot.status'].name_search('NEW')
        self.assertTrue(any(r[0] == self.status_1.id for r in result))
        
        # Test search by name
        result = self.env['stock.production.lot.status'].name_search('New Product')
        self.assertTrue(any(r[0] == self.status_1.id for r in result))
        
        # Test combined search
        result = self.env['stock.production.lot.status'].name_search('NEW Product')
        self.assertTrue(any(r[0] == self.status_1.id for r in result))

    def test_05_quant_status_compute(self):
        """Test compute status in stock quants"""
        quant = self.env['stock.quant'].create({
            'product_id': self.product.id,
            'location_id': self.stock_location.id,
            'lot_id': self.lot.id,
            'quantity': 1,
        })
        
        self.assertEqual(quant.status, f"{self.status_1.code} - {self.status_1.name}")

        # Test status update
        self.lot.status = self.status_2
        quant._compute_status()
        self.assertEqual(quant.status, f"{self.status_2.code} - {self.status_2.name}")

    def test_06_display_name_compute(self):
        """Test display name computation of production lot status"""
        self.assertEqual(
            self.status_1.display_name,
            f"{self.status_1.code}-{self.status_1.name}"
        )
