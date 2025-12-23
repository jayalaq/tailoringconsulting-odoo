from . import models
from . import reports
from odoo import api, SUPERUSER_ID

def _combined_post_init_hook(env):
    _register_hook_account_report_sale_14(env)
    _link_tags_ids(env)

def _register_hook_account_report_sale_14(env):
    
    existing_report = env['account.report'].search([('name', '=', 'VAT Report (RVIE Sales 14.4)')])
    existing_report_line = env['account.report.line'].search([('name', '=', 'RVIE 14.4')])

    if existing_report:
        additional_columns = [
            {
                'name': 'Asiento',
                'expression_label': 'move_name',
                'blank_if_zero': True,
            },
            {
                'name': 'Base Dscto IGV',
                'expression_label': 'base_igv_disc',
                'blank_if_zero': True,
            },
            {
                'name': 'Dscto IGV',
                'expression_label': 'tax_igv_disc',
                'blank_if_zero': True,
            },
            {
                'name': 'Otros Cargos',
                'expression_label': 'tax_other',
                'blank_if_zero': True,
            },
                
        ]
        existing_column_names = existing_report.column_ids.mapped('expression_label')
        columns_to_create = [
            col_data for col_data in additional_columns 
            if col_data['expression_label'] not in existing_column_names
        ]
        if columns_to_create:
            existing_report.write({
                'column_ids': [(0, 0, col_data) for col_data in columns_to_create]
            })
    if existing_report_line:
        existing_expression_labels = existing_report_line.expression_ids.mapped('label')
        if 'move_name' not in existing_expression_labels:
            existing_report_line.write({
                    'expression_ids': [(0, 0, {
                        'label': 'move_name',
                        'engine': 'custom',
                        'formula': '_report_custom_engine_ple_14_1',
                        'subformula': 'move_name',
                    })]
                })

def _link_tags_ids(env):

    def generate_tag_id(name):
        return env['account.account.tag'].search([('name', '=', '%s' % name)], limit=1)

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
    
    companies = env['res.company'].search([('chart_template', '=', 'pe')])
    for company in companies:
        for rec in type_acc:
            try:
                account = env.ref('account.%s_sale_tax_%s' % (company.id,rec))
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
