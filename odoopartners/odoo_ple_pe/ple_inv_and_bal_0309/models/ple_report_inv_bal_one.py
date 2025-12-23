from odoo import fields, models, api, _

class PleInvBal1One(models.Model):
    _inherit = 'ple.report.inv.bal.one'

    m2o_ple_report_inv_bal_09 = fields.Many2one('ple.report.inv.bal.09')
    txt_filename_309 = fields.Char(string='Filaname_09 .txt')
    txt_binary_309 = fields.Binary(string='Reporte .TXT 3.9')
    pdf_filename_309 = fields.Char(string='Filaname_09 .pdf')
    pdf_binary_309 = fields.Binary(string='Reporte .PDF 3.9')
    xls_filename_309 = fields.Char(string='Filaname_09 Excel')
    xls_binary_309 = fields.Binary(string='Reporte Excel')

    def create_book_09(self):
        self.m2o_ple_report_inv_bal_09 = self.env['ple.report.inv.bal.09'].create(
            {
                'company_id': self.company_id.id,
                'date_start': self.date_start,
                'date_end': self.date_end,
                'state_send': self.state_send,
                'date_ple': self.date_ple,
                'financial_statements_catalog': self.financial_statements_catalog,
                'eeff_presentation_opportunity': self.eeff_presentation_opportunity,
            }
        )

        self.m2o_ple_report_inv_bal_09.action_generate_excel()

        self.xls_filename_309 = self.m2o_ple_report_inv_bal_09.xls_filename_309
        self.xls_binary_309 = self.m2o_ple_report_inv_bal_09.xls_binary_309
        self.txt_filename_309 = self.m2o_ple_report_inv_bal_09.txt_filename_309
        self.txt_binary_309 = self.m2o_ple_report_inv_bal_09.txt_binary_309
        self.pdf_filename_309 = self.m2o_ple_report_inv_bal_09.pdf_filename_309
        self.pdf_binary_309 = self.m2o_ple_report_inv_bal_09.pdf_binary_309


    def action_generate_excel(self):
        self.create_book_09()
        super(PleInvBal1One, self).action_generate_excel()

    def action_rollback(self):
        self.m2o_ple_report_inv_bal_09.unlink()
        super(PleInvBal1One, self).action_rollback()