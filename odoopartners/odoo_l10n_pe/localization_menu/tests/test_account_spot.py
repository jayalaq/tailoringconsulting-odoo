from odoo.tests import common
from odoo import fields

@common.tagged('post_install', '-at_install')
class TestAccountSpot(common.TransactionCase):
    
    def setUp(self):
        super().setUp()
        self.account_spot_detraction = self.env['account.spot.detraction'].create({
            'name':'TestNameDetraction'
        })
        self.account_spot_retention = self.env['account.spot.retention'].create({
            'name':'TestNameRetention'
        })
        self.code_aduana = self.env['code.aduana'].create({
            'name':'testNameAduana',
            'code':'TEST-001'
        })
        
    def test_fields_account_spot(self):
        self.assertEqual(self.account_spot_detraction.name,'TestNameDetraction')
        self.assertEqual(self.account_spot_retention.name,'TestNameRetention')
        self.assertEqual(self.code_aduana.name,'testNameAduana')
        self.assertEqual(self.code_aduana.code,'TEST-001')
        