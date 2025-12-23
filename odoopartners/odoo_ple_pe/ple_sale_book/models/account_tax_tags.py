from odoo import _, models, api

class AccountTax(models.Model):
    _inherit = 'account.tax'

    @api.model
    def _link_tags_ids_update(self):

        def generate_tag_id(name):
            return self.env['account.account.tag'].search([('name', '=', '%s' % name)], limit=1)

        def set_tag_ids(account_tax, first, second):
            tags = []
            if first and account_tax.repartition_type == 'base':
                tags.append((4, generate_tag_id(first).id))
            if second and account_tax.repartition_type == 'tax':
                tags.append((4, generate_tag_id(second).id))
            account_tax.write({'tag_ids': [(5, 0, 0)] + tags}) 

        type_acc = ['igv_18', 'igv_18_included', 'exo', 'ina', 'ics_0', 'exp']
        tags_invoices = ['+S_BASE_OG', '+S_TAX_OG', '+S_BASE_OE', '+S_BASE_OU', '+S_TAX_ISC', '+S_BASE_EXP']
        tags_invoices_corrective = ['-S_BASE_OG', '-S_TAX_OG', '-S_BASE_OE', '-S_BASE_OU', '-S_TAX_ISC', '-S_BASE_EXP']
        
        companies = self.env['res.company'].search([('chart_template', '=', 'pe')])
        for company in companies:
            for rec in type_acc:
                try:
                    account = self.env.ref('account.%s_sale_tax_%s' % (company.id,rec))
                    if rec == 'igv_18':
                        for acc_tax in account.invoice_repartition_line_ids:
                            set_tag_ids(acc_tax, tags_invoices[0], tags_invoices[1])
                        for acc_tax in account.refund_repartition_line_ids:
                            set_tag_ids(acc_tax, tags_invoices_corrective[0], tags_invoices_corrective[1])
                    elif rec == 'igv_18_included':
                        for acc_tax in account.invoice_repartition_line_ids:
                            set_tag_ids(acc_tax, tags_invoices[0], tags_invoices[1])
                        for acc_tax in account.refund_repartition_line_ids:
                            set_tag_ids(acc_tax, tags_invoices_corrective[0], tags_invoices_corrective[1])
                    elif rec == 'exo':
                        for acc_tax in account.invoice_repartition_line_ids:
                            set_tag_ids(acc_tax, tags_invoices[2], False)
                        for acc_tax in account.refund_repartition_line_ids:
                            set_tag_ids(acc_tax, tags_invoices_corrective[2], False)
                    elif rec == 'ina':
                        for acc_tax in account.invoice_repartition_line_ids:
                            set_tag_ids(acc_tax, tags_invoices[3], False)
                        for acc_tax in account.refund_repartition_line_ids:
                            set_tag_ids(acc_tax, tags_invoices_corrective[3], False)
                    elif rec == 'ics_0':
                        for acc_tax in account.invoice_repartition_line_ids:
                            set_tag_ids(acc_tax, tags_invoices[4], False)
                        for acc_tax in account.refund_repartition_line_ids:
                            set_tag_ids(acc_tax, tags_invoices_corrective[4], False)
                    elif rec == 'exp':
                        for acc_tax in account.invoice_repartition_line_ids:
                            set_tag_ids(acc_tax, tags_invoices[5], False)
                        for acc_tax in account.refund_repartition_line_ids:
                            set_tag_ids(acc_tax, tags_invoices_corrective[5], False)
                except:
                    pass