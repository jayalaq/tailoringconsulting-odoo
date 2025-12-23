from odoo.tests.common import TransactionCase

class TestInvoiceCreation(TransactionCase):

    def setUp(self):
        super(TestInvoiceCreation, self).setUp()

        self.partner = self.env['res.partner'].create({
            'name': 'Test Partner',
            'vat': '20551583041', 
            'country_id': self.env.ref('base.pe').id,  
        })
        self.product = self.env['product.product'].create({
            'name': 'Test Product',
            'list_price': 100.0,
            'standard_price': 80.0,
        })

    def test_create_invoice(self):
        invoice = self.env['account.move'].create({
            'partner_id': self.partner.id,
            'move_type': 'out_invoice',
            'carrier_ref_number': '123456789012345678901234567890',  
            'invoice_line_ids': [(0, 0, {
                'product_id': self.product.id,
                'quantity': 1.0,
                'price_unit': 85.0,
            })]
        })

        self.assertTrue(invoice, "La factura no se ha creado.")
        self.assertEqual(invoice.partner_id.name, 'Test Partner', "El cliente de la factura no es correcto.")
        self.assertEqual(invoice.amount_total, 100.3, "El total de la factura no es correcto.")
        self.assertEqual(invoice.state, 'draft', "El estado inicial de la factura debería ser 'draft'.")

        # Confirmar la factura para forzar la creación del archivo XML
        invoice.action_post()

        edi_model = self.env['account.edi.xml.ubl_pe']
        exported_vals = edi_model._export_invoice_vals(invoice)

        despatch_document_reference = exported_vals['vals'].get('despatch_document_reference')
        self.assertIsNotNone(despatch_document_reference, "El campo 'despatch_document_reference' no fue generado.")
        self.assertEqual(despatch_document_reference, '123456789012345678901234567890', "El valor de 'despatch_document_reference' no es correcto.")

        despatch_document_reference_type_code = exported_vals['vals'].get('despatch_document_reference_type_code')
        self.assertEqual(despatch_document_reference_type_code, '09', "El código de tipo de 'despatch_document_reference' no es correcto.")
        
        print("--------- <<<<<<   TEST 1  >>>>>> ---------")

