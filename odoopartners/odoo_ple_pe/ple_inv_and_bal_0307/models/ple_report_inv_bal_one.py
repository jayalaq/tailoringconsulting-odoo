from odoo import fields, models


class PleInvBal1One(models.Model):
    _inherit = 'ple.report.inv.bal.one'

    xls_filename_07 = fields.Char(string='Filaname_07 .xls')
    xls_binary_07 = fields.Binary(string='Reporte .XLS 3.7')
    txt_filename_07 = fields.Char(string='Filaname_07 .txt')
    txt_binary_07 = fields.Binary(string='Reporte .TXT 3.7')
    pdf_filename_07 = fields.Char(string='Filaname_07 .pdf')
    pdf_binary_07 = fields.Binary(string='Reporte .PDF 3.7')
    ple_report_inv_bal_07_id = fields.Many2one('ple.report.inv.bal.07')

    def create_book_07(self):
        self.ple_report_inv_bal_07_id = self.env["ple.report.inv.bal.07"].create({
            'company_id': self.company_id.id,
            'date_start': self.date_start,
            'date_end': self.date_end,
            'state_send': self.state_send,
            'date_ple': self.date_ple,
            'financial_statements_catalog': self.financial_statements_catalog,
            'eeff_presentation_opportunity': self.eeff_presentation_opportunity,
        })
        self.ple_report_inv_bal_07_id.action_generate_excel()

        self.xls_filename_07 = self.ple_report_inv_bal_07_id.xls_filename
        self.xls_binary_07 = self.ple_report_inv_bal_07_id.xls_binary
        self.txt_filename_07 = self.ple_report_inv_bal_07_id.txt_filename
        self.txt_binary_07 = self.ple_report_inv_bal_07_id.txt_binary
        self.pdf_filename_07 = self.ple_report_inv_bal_07_id.pdf_filename
        self.pdf_binary_07 = self.ple_report_inv_bal_07_id.pdf_binary

        self.ple_report_inv_bal_07_id.xls_binary = False
        self.ple_report_inv_bal_07_id.txt_binary = False
        self.ple_report_inv_bal_07_id.pdf_binary = False

    def action_generate_excel(self):
        self.create_book_07()
        super(PleInvBal1One, self).action_generate_excel()

    def action_rollback(self):
        self.ple_report_inv_bal_07_id.unlink()
        super(PleInvBal1One, self).action_rollback()
