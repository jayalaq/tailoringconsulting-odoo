from odoo.tests.common import TransactionCase
from odoo.tests import tagged
from datetime import *

@tagged('post_install', '-at_install')
class TestAssetIntangible(TransactionCase):

    def setUp(self):
        super().setUp()
        
        self.asset = self.env['asset.intangible'].create({
            'name':'Test Asset Intan',
            'bool_asset_intagible':True,
            'operation_date':date.today()
        })
        
    def test_asset_intangible(self):
        asset_id = self.asset._name_search(
            name='Test Asset Intan', 
            args=None, 
            operator='ilike', 
            limit=100, 
            name_get_uid=None)
        assets = self.env['asset.intangible'].browse(asset_id)
        
        self.assertEqual(self.asset.name,assets.name)
        self.assertEqual(self.asset.operation_date,assets.operation_date)
        self.assertEqual(self.asset.bool_asset_intagible,assets.bool_asset_intagible)