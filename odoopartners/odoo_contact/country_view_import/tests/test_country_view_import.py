from odoo.tests import tagged
from odoo.tests.common import TransactionCase


@tagged('country_view_import', 'post_install', '-at_install', '-standard')
class TestCountryViewImport(TransactionCase):

    def test_country_view_inherit(self):
        country_view_tree = self.env.ref('base.view_country_tree')
        country_template = self.env['ir.ui.view'].sudo()._read_template(country_view_tree.id)
        country_template_expected = """
            <tree string="Country" create="1" delete="1">
                <field name="name"/>
                <field name="code"/>
            </tree>
        """
        self.assertXMLEqual(country_template, country_template_expected)
