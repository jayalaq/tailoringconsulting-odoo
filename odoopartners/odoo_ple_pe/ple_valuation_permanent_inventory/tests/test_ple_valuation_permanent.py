from odoo.tests.common import TransactionCase
from odoo.tests import tagged
from datetime import date,timedelta
import logging
_logger = logging.getLogger(__name__)


@tagged('post_install', '-at_install')
class TestPleValuationPermanent(TransactionCase):
    
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
        _logger.info('==== Test Generate Order Purchase OK ====')
    
    def test_generate_report_ple_valuation(self):
        # Create record ple_permanent_inventory_physical_units 
        record_ple_permanent_units = self.ple_permanent_units.create({
            'company_id':self.env['res.company'].search([])[0].id,
            'date_start': date.today() - timedelta(days=1),
            'date_end':  date.today() +  timedelta(days=1),
            'state_send': '1',
        })
        
        # Before Generate report
        self.assertTrue(record_ple_permanent_units)
        self.assertFalse(record_ple_permanent_units.xls_filename_valued)
        self.assertFalse(record_ple_permanent_units.txt_filename_valued)

        record_ple_permanent_units.action_calc_balance()
        record_ple_permanent_units.action_generate_report_valued()
        # After Generate report
        
        self.assertTrue(record_ple_permanent_units)
        self.assertTrue(record_ple_permanent_units.xls_filename_valued)
        self.assertTrue(record_ple_permanent_units.txt_filename_valued)
        _logger.info('===== Test Generate Report Ple Valuation Permanent  =====')