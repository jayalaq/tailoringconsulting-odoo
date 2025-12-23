from odoo import api, models

from odoo.addons.account.models.chart_template import template


class AccountChartTemplate(models.AbstractModel):
    _inherit = 'account.chart.template'

    @api.model
    def _edocument_post_init(self):
        queries = [
            """UPDATE account_tax SET sequence = 8, name = jsonb_build_object('en_US', '0% Free Transfer','es_PE', '0% Transferencia Gratuita'), l10n_pe_edi_unece_category = 'Z', l10n_pe_edi_affectation_reason = '21', amount = 100	WHERE id IN (SELECT res_id FROM ir_model_data WHERE model = 'account.tax' AND module = 'account' AND name = '1_sale_tax_gra')""",
            """DELETE FROM account_tax_repartition_line WHERE document_type = 'refund' AND tax_id IN (SELECT res_id FROM ir_model_data WHERE model = 'account.tax' AND module = 'account' AND name = '1_sale_tax_gra')""",
            """DELETE FROM account_tax_repartition_line WHERE document_type = 'invoice' AND tax_id IN (SELECT res_id FROM ir_model_data WHERE model = 'account.tax' AND module = 'account' AND name = '1_sale_tax_gra')""",
            """INSERT INTO account_tax_repartition_line (document_type,tax_id,account_id,company_id,sequence,repartition_type,use_in_tax_closing,create_date, write_date,factor_percent) VALUES('invoice',(SELECT res_id FROM ir_model_data WHERE model = 'account.tax' AND module = 'account' AND name = '1_sale_tax_gra'),null, (SELECT COMPANY_ID FROM ACCOUNT_TAX where id in (SELECT res_id FROM ir_model_data WHERE model = 'account.tax' AND module = 'account' AND name = '1_sale_tax_gra')), 1, 'base', false,CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, 0)""",
            """INSERT INTO account_tax_repartition_line (document_type,tax_id,account_id,company_id,sequence,repartition_type,use_in_tax_closing,create_date, write_date,factor_percent) VALUES('invoice',(SELECT res_id FROM ir_model_data WHERE model = 'account.tax' AND module = 'account' AND name = '1_sale_tax_gra'),null,  (SELECT COMPANY_ID FROM ACCOUNT_TAX where id in (SELECT res_id FROM ir_model_data WHERE model = 'account.tax' AND module = 'account' AND name = '1_sale_tax_gra')), 2, 'tax', false, CURRENT_TIMESTAMP,CURRENT_TIMESTAMP, -100)""",
            """INSERT INTO account_tax_repartition_line (document_type,tax_id,account_id,company_id,sequence,repartition_type,use_in_tax_closing,create_date, write_date,factor_percent) VALUES('refund',(SELECT res_id FROM ir_model_data WHERE model = 'account.tax' AND module = 'account' AND name = '1_sale_tax_gra'), null, (SELECT COMPANY_ID FROM ACCOUNT_TAX where id in (SELECT res_id FROM ir_model_data WHERE model = 'account.tax' AND module = 'account' AND name = '1_sale_tax_gra')), 1, 'base', false, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, 0)""",
            """INSERT INTO account_tax_repartition_line (document_type,tax_id,account_id,company_id,sequence,repartition_type,use_in_tax_closing,create_date, write_date,factor_percent) VALUES('refund',(SELECT res_id FROM ir_model_data WHERE model = 'account.tax' AND module = 'account' AND name = '1_sale_tax_gra'),null,  (SELECT COMPANY_ID FROM ACCOUNT_TAX where id in (SELECT res_id FROM ir_model_data WHERE model = 'account.tax' AND module = 'account' AND name = '1_sale_tax_gra')), 2, 'tax', false, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, -100)"""
        ]

        all_companies = self.env['res.company'].search([('chart_template', '=', 'pe')])
        for company in all_companies:
            Template = self.with_company(company)
            Template._load_data({'account.tax': self._get_pe_new_account_tax()})
            for query in queries:
                Template._cr.execute(query)
        return True

    @template('pe', 'account.tax')
    def _get_pe_new_account_tax(self):
        return self._parse_csv('pe', 'account.tax', module='l10n_pe_edocument')
