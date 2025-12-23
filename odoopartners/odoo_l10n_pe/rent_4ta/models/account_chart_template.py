from odoo import models, api
from odoo.addons.account.models.chart_template import template

class AccountChartTemplate(models.AbstractModel):
    _inherit = 'account.chart.template'

    @template('pe', 'account.tax.group')
    def _get_pe_rent_4ta_group_tax(self):
        tax_groups = self._parse_csv('pe', 'account.tax.group', module='rent_4ta')
        return tax_groups

    @template('pe', 'account.tax')
    def _get_pe_rent_4ta_tax(self):
        taxes = self._parse_csv('pe', 'account.tax', module='rent_4ta')
        return taxes
    
    @api.model
    def rent_4ta_post_init(self):
        all_companies = self.env['res.company'].search([('chart_template', '=', 'pe')])
        for company in all_companies:
            Template = self.with_company(company)
            Template._load_data({'account.tax.group': self._get_pe_rent_4ta_group_tax()})
            Template._load_data({'account.tax': self._get_pe_rent_4ta_tax()})
        return True


