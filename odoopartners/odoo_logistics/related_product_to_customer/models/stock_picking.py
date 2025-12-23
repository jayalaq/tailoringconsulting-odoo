from odoo import api, models
from lxml import etree


class StockPicking(models.Model):
    _inherit = 'stock.picking'
    
    @api.model
    def get_views(self, views, options=None):
        res = super().get_views(views, options)
        if 'form' in res['views']:
            arch = res['views']['form']['arch']
            arch_tree = etree.fromstring(arch)
            subtree = arch_tree.xpath("//field[@name='product_id']")
            if subtree:
                domain = "['|', ('partner_ids', 'in', parent.partner_id), ('partner_ids', '=', False)]"
                subtree[0].set('domain', domain)
                res['views']['form']['arch'] = etree.tostring(arch_tree, encoding='unicode')
        return res
