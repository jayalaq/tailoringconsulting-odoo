from odoo.tests import tagged
from odoo.tests.common import TransactionCase
from odoo.exceptions import AccessError


@tagged('-at_install', 'post_install')
class TestPrintAditionalComment(TransactionCase):

    @classmethod
    def setUpClass(self):
        super(TestPrintAditionalComment, self).setUpClass()
        self.company_temp = self.env['res.company'].search([])[0]
        self.invoice_temp = self.env['account.move'].search([])[0]

    def test_print_additional_comment(self):
        self.company_temp.additional_information = 'Información adicional de prueba !!'
        self.assertEqual(
            self.company_temp.additional_information,
            '<p>Información adicional de prueba !!</p>',
            'No se ha guardado correctamente el campo de informacion adicional'
        )

    def test_print_additional_comment_report_invoice(self):
        self.invoice_temp.company_id.additional_information = 'Información adicional de prueba !!'
        self.assertEqual(
            self.invoice_temp.company_id.additional_information,
            '<p>Información adicional de prueba !!</p>',
            'No se ha guardado correctamente el campo de informacion adicional'
        )
        self.assertRaises(AccessError, self.invoice_temp.action_post())
        self.env['ir.actions.report']._render('account.account_invoices', self.invoice_temp.ids)[0]
        pdf_name = self.invoice_temp._get_invoice_report_filename()
        self.assertEqual(
            pdf_name,
            'B BOL-00000001.pdf',
            'No se ha generado el PDF correctamente'
        )
