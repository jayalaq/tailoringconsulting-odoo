from datetime import date,timedelta
from odoo.tests.common import TransactionCase
from odoo.tests import tagged
 
class TestStockProductsValuationFinal(TransactionCase):

    def setUp(self):
        super().setUp()
        self.StockProductsValuationFinal = self.env["ple.stock.products.valuation.final"]

    def test_compute_total_value(self):
        "Check _compute_total_value method"
        quantity_product_hand = 10.0
        standard_price = 20.0
        expected_total_value = quantity_product_hand * standard_price
        product_valuation_final = self.StockProductsValuationFinal.create({
            'quantity_product_hand': quantity_product_hand,
            'standard_price': standard_price,
        })
        self.assertEqual(product_valuation_final.total_value,
                         expected_total_value)

        print("Test compute_total_value StockProductsValuationFinal OK ...... !!!!")
        print("======================== Test StockProductsValuationFinal OK ========================")


class TestPlePermanentFinal(TransactionCase):

    def setUp(self):
        super().setUp()
        self.PlePermanentFinal = self.env["ple.permanent.inventory.physical.units"]

    def test_generete_ending_balances(self):
        "Check generete_ending_balances method"
        date_start = date(2023, 1, 1)
        date_end = date(2023, 12, 31)
        company_id = 1
        inventory = self.PlePermanentFinal.create({
            'date_start': date_start,
            'date_end': date_end,
            'company_id': company_id,
            'state': 'load',
            'state_send': '1',

        })
        inventory.generete_ending_balances()

        print("Test generete_ending_balances PlePermanentFinal OK ...... !!!!")

    def test_opening_balances(self):
        "Check opening_balances method"
        product = 1
        quantity_hand = {
            'quantity_product_hand': 10.0,
            'product_valuation': 'Product A',
            'udm_product': 'uom',
            'standard_price': 20.0,
            'total_value': 200.0,
            'code_exist': 1,
        }
        year = '2023'
        month = '01'
        day = '01'
        correct_name = 'Product A'
        inventory = self.PlePermanentFinal.create({
            'state': 'draft',
            'state_send': '1',
            'date_start': '2021-01-01',
            'date_end': '2021-01-31',
        })
        inventory.opening_balances(
            product, quantity_hand, year, month, day, correct_name=correct_name
        )

        print("Test opening_balances PlePermanentFinal OK ...... !!!!")
        print('======================== Test PlePermanentFinal OK ========================')

@tagged('post_install', '-at_install')
class TestPlePermanentGeneral(TransactionCase):
    
    def setUp(self):
        super().setUp()
        # Create record partner
        self.partner = self.env['res.partner'].create({
            'name':'Ferretería Caviedes SA',
        })
        # Create record product_category
        self.product_category = self.env['product.category'].create({
            'name':'Tintes',
            'property_cost_method':'average',
            'property_valuation':'real_time'
        })
        # Create record product_template
        self.product_template = self.env['product.template'].create({
            'name':'Tinte Mate especial para acero',
            'sale_ok':True,
            'purchase_ok':True,
            'detailed_type':'product',
            'uom_id':self.env['uom.uom'].search([])[0].id,
            'uom_po_id':self.env['uom.uom'].search([])[0].id,
            'categ_id':self.product_category.id,
            'list_price':20,
            'standard_price':11.002599
        })
           
        self.ple_permanent_units = self.env["ple.permanent.inventory.physical.units"]

      
    def test_purchase_order_ple(self):
        # Create Order Purchase
        purchase_order = self.env['purchase.order'].create({
            'partner_id': self.partner.id,
            'order_line':[(0,0,{
                'product_id':self.product_template.id,
                'product_qty': 1199,
                'price_unit':self.product_template.standard_price
            })]
        })
        
        order = purchase_order.button_confirm()
        stock_picking = self.env['stock.picking'].search([('partner_id','=',purchase_order.partner_id.id)])
        pick = stock_picking.button_validate()
        
        self.assertTrue(order,'Error the confirm the purchase')
        self.assertTrue(pick,'Error the validate the picking')
        self.assertEqual(purchase_order.partner_id.id,self.partner.id)
        print("======================== Test Generate Order Purchase OK ========================")

        
    def test_generate_report_ple_permanent(self):
        # Create record ple_permanent_inventory_physical_units 
        record_ple_permanent_units = self.ple_permanent_units.create({
            'company_id':self.env['res.company'].search([])[0].id,
            'date_start': date.today() - timedelta(days=1),
            'date_end':  date.today() +  timedelta(days=1),
            'state_send': '1',
        })
        
        # Before Generate report
        self.assertTrue(record_ple_permanent_units)
        self.assertFalse(record_ple_permanent_units.xls_filename)
        self.assertFalse(record_ple_permanent_units.txt_filename)
        self.assertFalse(record_ple_permanent_units.date_ple)
        self.assertEqual(record_ple_permanent_units.state,'draft')

        record_ple_permanent_units.action_calc_balance()
        record_ple_permanent_units.action_generate_report()
        # After Generate report
        
        self.assertTrue(record_ple_permanent_units)
        self.assertTrue(record_ple_permanent_units.xls_filename)
        self.assertTrue(record_ple_permanent_units.txt_filename)
        self.assertEqual(record_ple_permanent_units.date_ple,date.today())
        self.assertEqual(record_ple_permanent_units.state,'load')

        print("============== Test Generate Report Ple Permanent Inventory Physical Units ==============")
