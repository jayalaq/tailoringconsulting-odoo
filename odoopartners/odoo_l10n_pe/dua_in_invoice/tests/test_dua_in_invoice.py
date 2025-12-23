from odoo.tests import tagged
from odoo.tests.common import TransactionCase

@tagged('-at_install', 'post_install')
class TestDuaInInvoice(TransactionCase):

    def setUp(self):
        super(TestDuaInInvoice, self).setUp()
        self.product = self.env['product.product'].create({'name': 'Producto de Prueba'})

    def test_aduana_fields_activation(self):
        document_type_01 = self.env['l10n_latam.document.type'].search([('code', '=', '01')], limit=1)
        document_type_50 = self.env['l10n_latam.document.type'].search([('code', '=', '50')], limit=1)
        code_aduana = self.env['code.aduana'].search([('code', '=', '19')], limit=1)

        # Factura con tipo de documento diferente de 50
        invoice_01 = self.env['account.move'].create({
            'partner_id': self.env.ref('base.partner_admin').id,
            'move_type': 'in_invoice',
            'invoice_date': '2024-02-01',
            'invoice_line_ids': [(0, 0, {'product_id': self.product.id, 'quantity': 1, 'price_unit': 100})],
            'l10n_latam_document_type_id': document_type_01.id
        })
        self.assertFalse(invoice_01.year_aduana, "El campo year_aduana no está activo cuando no debería.")
        self.assertFalse(invoice_01.code_aduana, "El campo code_aduana no está activo cuando no debería.")

        # Factura con tipo de documento igual a 50
        invoice_50 = self.env['account.move'].create({
            'partner_id': self.env.ref('base.partner_admin').id,
            'move_type': 'in_invoice',
            'invoice_date': '2024-02-01',
            'invoice_line_ids': [(0, 0, {'product_id': self.product.id, 'quantity': 1, 'price_unit': 100})],
            'l10n_latam_document_type_id': document_type_50.id,
            'year_aduana': '2020',
            'code_aduana': code_aduana.id,
        })
        self.assertTrue(invoice_50.year_aduana, "El campo year_aduana está activo cuando debería.")
        self.assertTrue(invoice_50.code_aduana, "El campo code_aduana está activo cuando debería.")

        print('-------------TEST OK-------------')

