from odoo.tests import common, tagged
from odoo.exceptions import AccessError

@tagged('post_install', '-at_install')
class TestViewInventoryButton(common.TransactionCase):
    def setUp(self):
        super(TestViewInventoryButton, self).setUp()
        # Create test users
        self.test_user = self.env['res.users'].create({
            'name': 'Test User',
            'login': 'test_user',
            'email': 'test@example.com',
            'groups_id': [(6, 0, [self.env.ref('base.group_user').id])]
        })
        
        self.test_user_with_rights = self.env['res.users'].create({
            'name': 'Test User With Rights',
            'login': 'test_user_rights',
            'email': 'test_rights@example.com',
            'groups_id': [(6, 0, [
                self.env.ref('base.group_user').id,
                self.env.ref('view_inventory_button.group_enable_non_editable_stock_product_buttons').id
            ])]
        })

        # Create test product
        self.test_product = self.env['product.template'].create({
            'name': 'Test Product',
            'type': 'product',
            'responsible_id': self.test_user_with_rights,
            'tracking': 'none'
        })
        # Create test product
        self.test_product_service = self.env['product.template'].create({
            'name': 'Test Product',
            'type': 'service',
            'tracking': 'none'
        })

    def test_01_menu_access_rights(self):
        """Test access to stock menu based on group rights"""
        stock_menu = self.env.ref('stock.menu_stock_root')
        
        # Test for user without rights
        menus_user = self.env['ir.ui.menu'].with_user(self.test_user.id).get_user_roots()
        self.assertNotIn(
            stock_menu.id,
            menus_user.ids,
            "Stock menu should not be accessible to user without rights"
        )

    def test_02_update_quantity_button_visibility(self):
        """Test visibility of Update Quantity button"""
        # Test for user without rights
        product = self.test_product.with_user(self.test_user.id)
        self.assertFalse(
            self.test_user.has_group('view_inventory_button.group_enable_non_editable_stock_product_buttons'),
            "User should not have rights to see inventory buttons"
        )

        # Test for user with rights
        product = self.test_product.with_user(self.test_user_with_rights.id)
        self.assertTrue(
            self.test_user_with_rights.has_group('view_inventory_button.group_enable_non_editable_stock_product_buttons'),
            "User should have rights to see inventory buttons"
        )

    def test_03_product_smart_buttons(self):
        """Test visibility and functionality of product smart buttons"""
        product = self.test_product.with_user(self.test_user_with_rights.id)
        
        # Test On Hand button visibility
        self.assertTrue(product.show_on_hand_qty_status_button, 
                       "On Hand quantity button should be visible for products")
        
        # Test Forecasted button visibility
        self.assertTrue(product.show_forecasted_qty_status_button, 
                       "Forecasted quantity button should be visible for products")

    def test_04_lot_serial_button_visibility(self):
        """Test visibility of Lot/Serial Numbers button based on tracking setting"""
        # Test with no tracking
        self.assertFalse(self.test_product.tracking != 'none', 
                        "Lot/Serial button should not be visible when tracking is none")

        # Test with lot tracking
        self.test_product.tracking = 'lot'
        self.assertTrue(self.test_product.tracking != 'none', 
                       "Lot/Serial button should be visible when tracking is enabled")

    def test_05_responsible_field_access(self):
        """Test access to responsible_id field"""
        # Test user with rights can set responsible
        product = self.test_product.with_user(self.test_user_with_rights.id)
        self.assertEqual(product.responsible_id.id, self.test_user_with_rights.id,
                        "Should be able to set responsible when user has rights")

        # Test user without rights cannot set responsible
        product = self.test_product.with_user(self.test_user.id)
        with self.assertRaises(AccessError):
            product.responsible_id = self.test_user.id

    def test_06_putaway_rules_button(self):
        """Test visibility and access to putaway rules button"""
        product = self.test_product_service.with_user(self.test_user_with_rights.id)

        self.assertEqual(product.type, 'service',
                        "Putaway rules button should not be visible for service products")
