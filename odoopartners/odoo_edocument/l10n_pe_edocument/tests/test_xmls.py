from odoo.tests.common import TransactionCase
from lxml import etree


class TestInvoiceCreation(TransactionCase):
    def setUp(self):
        super(TestInvoiceCreation, self).setUp()
        self.partner = self.env['res.partner'].create({
            'name': 'Test Partner',
            'vat': '20551583041',
            'country_id': self.env.ref('base.pe').id,
        })
        self.tax_free = self.env['account.tax'].search([('name', '=', '0% Transferencia Gratuita')], limit=1)
        self.tax_18 = self.env['account.tax'].search([('id', '=', 1)], limit=1)
        self.tax_18_ttc = self.env['account.tax'].search([('id', '=', 2)], limit=1)
        self.product_with_detraction = self.env['product.template'].create({
            'name': 'Raspberry with config detraction',
            'detailed_type': 'service',
            'type': 'service',
            'invoice_policy': 'order',
            'standard_price': 0,
            'sale_ok': True,
            'purchase_ok': True,
            'list_price': 100.0,
            'uom_id': self.env.ref('uom.product_uom_unit').id,
            'uom_po_id': self.env.ref('uom.product_uom_unit').id,
            'taxes_id': [(4, self.tax_18.id)],
            'l10n_pe_withhold_code': '037',  # codigo de detracción
            'l10n_pe_withhold_percentage': 12,  # porcentaje de detracción
        })

        self.products = self.env['product.product'].create([
            {
                'name': f'Test Product {i}',
                'list_price': 100.0,
                'standard_price': 80.0,
            } for i in range(1, 4)
        ])

    def _create_invoice(self, lines):
        return self.env['account.move'].create({
            'partner_id': self.partner.id,
            'move_type': 'out_invoice',
            'l10n_pe_edi_operation_type': "0101",
            'invoice_line_ids': lines
        })

    def _get_xml_content(self, invoice):
        edi_format = self.env.ref('l10n_pe_edi.edi_pe_ubl_2_1')
        return edi_format._l10n_pe_edi_xml_invoice_content(invoice)

    def _assert_xml_node(self, node, xpath, expected_value, message):
        elements = node.findall(xpath)
        self.assertIsNotNone(elements, f"{message}: Nodes {xpath} not found.")
        for element, expected_value in zip(elements, expected_value):
            self.assertEqual(element.text, expected_value, f"{message}: Value of {xpath} is not as expected.")

    def test_create_invoice_with_free_transfer(self):

        invoice_lines = [
            (0, 0, {'product_id': self.products[0].id, 'quantity': 1.0, 'price_unit': 100, 'tax_ids': [(4, self.tax_free.id)]})
        ]

        invoice = self._create_invoice(invoice_lines)
        invoice.action_post()

        xml_content = self._get_xml_content(invoice)
        root = etree.fromstring(xml_content.decode())

        # Verificamos TaxTotal
        self._assert_xml_node(root, ".//{*}TaxTotal//{*}TaxAmount", ['0.00'], "TaxAmount")
        self._assert_xml_node(root, ".//{*}TaxTotal//{*}TaxSubtotal//{*}TaxAmount", ['0.00'], "TaxSubtotal Amount")
        self._assert_xml_node(root, ".//{*}TaxTotal//{*}TaxSubtotal//{*}TaxableAmount", ['100.00'], "TaxSubtotal TaxableAmount")

        # Verificamos LegalMonetaryTotal
        for tag in ["LineExtensionAmount", "TaxInclusiveAmount", "PayableAmount", "TaxExclusiveAmount", "PrepaidAmount"]:
            self._assert_xml_node(root, f".//{{*}}LegalMonetaryTotal//{{*}}{tag}", ['0.00'], f"LegalMonetaryTotal {tag}")

        # Verificamos InvoiceLine
        self._assert_xml_node(root, ".//{*}InvoiceLine//{*}TaxTotal//{*}TaxAmount", ['0.00'], "TaxAmount")
        self._assert_xml_node(root, ".//{*}InvoiceLine//{*}TaxTotal//{*}TaxSubtotal//{*}TaxCategory//{*}Percent", ['100.0'], "Percent")
        self._assert_xml_node(root, ".//{*}InvoiceLine//{*}TaxTotal//{*}TaxSubtotal//{*}TaxCategory//{*}TaxExemptionReasonCode", ['21'], "TaxExemptionReasonCode")
        self._assert_xml_node(root, ".//{*}InvoiceLine//{*}TaxTotal//{*}TaxSubtotal//{*}TaxCategory//{*}TaxScheme//{*}ID", ['9996'], "TaxSchemeID")
        self._assert_xml_node(root, ".//{*}InvoiceLine//{*}TaxTotal//{*}TaxSubtotal//{*}TaxCategory//{*}TaxScheme//{*}Name", ['GRA'], "TaxSchemeName")
        self._assert_xml_node(root, ".//{*}InvoiceLine//{*}TaxTotal//{*}TaxSubtotal//{*}TaxCategory//{*}TaxScheme//{*}TaxTypeCode", ['FRE'], "TaxTypeCode")
        self._assert_xml_node(root, ".//{*}InvoiceLine//{*}Price//{*}PriceAmount", ['0.0'], "PriceAmount")

        print("--------- TEST 1 COMPLETED SUCCESSFULLY ---------")

    def test_create_invoice_with_free_transfer_and_different_tax(self):
        invoice_lines = [
            (0, 0, {'product_id': self.products[0].id, 'quantity': 1.0, 'price_unit': 100.0}),
            (0, 0, {'product_id': self.products[1].id, 'quantity': 1.0, 'price_unit': 100.0}),
            (0, 0, {'product_id': self.products[2].id, 'quantity': 1.0, 'price_unit': 100.0, 'tax_ids': [(4, self.tax_free.id)]})
        ]
        invoice = self._create_invoice(invoice_lines)
        invoice.action_post()

        xml_content = self._get_xml_content(invoice)
        root = etree.fromstring(xml_content.decode())

        # Verificamos TaxTotal
        self._assert_xml_node(root, ".//{*}TaxTotal//{*}TaxAmount", ['36.00'], "TaxAmount")
        self._assert_xml_node(root, ".//{*}TaxTotal//{*}TaxSubtotal//{*}TaxableAmount", ['200.00', '100.00'], "TaxSubtotal TaxableAmount")
        self._assert_xml_node(root, ".//{*}TaxTotal//{*}TaxSubtotal//{*}TaxAmount", ['36.00', '0.00'], "TaxSubtotal Amount")
        self._assert_xml_node(root, ".//{*}TaxTotal//{*}TaxSubtotal//{*}TaxCategory//{*}TaxScheme//{*}ID", ['1000', '9996'], "ID")
        self._assert_xml_node(root, ".//{*}TaxTotal//{*}TaxSubtotal//{*}TaxCategory//{*}TaxScheme//{*}Name", ['IGV', 'GRA'], "Name")
        self._assert_xml_node(root, ".//{*}TaxTotal//{*}TaxSubtotal//{*}TaxCategory//{*}TaxScheme//{*}TaxTypeCode", ['VAT', 'FRE'], "TaxTypeCode")

        # Verificamos LegalMonetaryTotal
        self._assert_xml_node(root, ".//{*}LegalMonetaryTotal//{*}LineExtensionAmount", ['200.00'], "LineExtensionAmount")
        self._assert_xml_node(root, ".//{*}LegalMonetaryTotal//{*}TaxExclusiveAmount", ['200.00'], "TaxExclusiveAmount")
        self._assert_xml_node(root, ".//{*}LegalMonetaryTotal//{*}TaxInclusiveAmount", ['236.00'], "TaxInclusiveAmount")
        self._assert_xml_node(root, ".//{*}LegalMonetaryTotal//{*}PrepaidAmount", ['0.00'], "PrepaidAmount")
        self._assert_xml_node(root, ".//{*}LegalMonetaryTotal//{*}PayableAmount", ['236.00'], "PayableAmount")

        # Verificamos InvoiceLine
        self._assert_xml_node(root, ".//{*}InvoiceLine//{*}TaxTotal//{*}TaxAmount", ['18.00', '18.00', '18.00', '18.00', '0.00', '0.00'], "TaxAmount")
        self._assert_xml_node(root, ".//{*}InvoiceLine//{*}TaxTotal//{*}TaxSubtotal//{*}TaxCategory//{*}Percent", ['18.0', '18.0', '100.0'], "Percent")
        self._assert_xml_node(root, ".//{*}InvoiceLine//{*}TaxTotal//{*}TaxSubtotal//{*}TaxCategory//{*}TaxExemptionReasonCode", ['10', '10', '21'], "TaxExemptionReasonCode")
        self._assert_xml_node(root, ".//{*}InvoiceLine//{*}TaxTotal//{*}TaxSubtotal//{*}TaxCategory//{*}TaxScheme//{*}ID", ['1000', '1000', '9996'], "ID")
        self._assert_xml_node(root, ".//{*}InvoiceLine//{*}TaxTotal//{*}TaxSubtotal//{*}TaxCategory//{*}TaxScheme//{*}Name", ['IGV', 'IGV', 'GRA'], "Name")
        self._assert_xml_node(root, ".//{*}InvoiceLine//{*}TaxTotal//{*}TaxSubtotal//{*}TaxCategory//{*}TaxScheme//{*}TaxTypeCode", ['VAT', 'VAT', 'FRE'], "TaxTypeCode")
        self._assert_xml_node(root, ".//{*}InvoiceLine//{*}Price//{*}PriceAmount", ['100.0', '100.0', '0.0'], "PriceAmount")

        print("--------- TEST 2 COMPLETED SUCCESSFULLY ---------")

    def test_create_invoice_withdrawal_prize(self):
        """
        Este tests crea una factura con 3 lineas, 2 lineas con impuesto 18% y una linea con impuesto 18% Retiro - Retiro por premio
        """
        tax_test3 = self.env['account.tax'].search(
            [('name', '=', '18% Retiro - Retiro por premio')],limit=1)

        invoice_lines = [
            (0, 0, {'product_id': self.products[0].id, 'quantity': 1.0, 'price_unit': 100.0}),
            (0, 0, {'product_id': self.products[1].id, 'quantity': 1.0, 'price_unit': 100.0}),
            (0, 0, {'product_id': self.products[2].id, 'quantity': 1.0, 'price_unit': 100.0, 'tax_ids': [(4, tax_test3.id)]})
        ]
        invoice = self._create_invoice(invoice_lines)

        invoice.action_post()

        xml_content = self._get_xml_content(invoice)
        root = etree.fromstring(xml_content.decode())

        # Verificamos TaxTotal
        self._assert_xml_node(root, ".//{*}TaxTotal//{*}TaxAmount", ['36.00'], "TaxTotal Amount")
        self._assert_xml_node(root, ".//{*}TaxTotal//{*}TaxSubtotal//{*}TaxAmount", ['36.00', '18.00'], "TaxSubtotal Amount")
        self._assert_xml_node(root, ".//{*}TaxTotal//{*}TaxSubtotal//{*}TaxableAmount", ['200.00', '100.00'], "TaxSubtotal TaxableAmount")
        self._assert_xml_node(root, ".//{*}TaxTotal//{*}TaxSubtotal//{*}TaxCategory//{*}TaxScheme//{*}ID", ['1000', '9996'], "TaxSchemeID")
        self._assert_xml_node(root, ".//{*}TaxTotal//{*}TaxSubtotal//{*}TaxCategory//{*}TaxScheme//{*}Name", ['IGV', 'GRA'], "TaxSchemeName")
        self._assert_xml_node(root, ".//{*}TaxTotal//{*}TaxSubtotal//{*}TaxCategory//{*}TaxScheme//{*}TaxTypeCode", ['VAT', 'FRE'], "TaxTypeCode")

        # Verificamos LegalMonetaryTotal
        self._assert_xml_node(root, ".//{*}LegalMonetaryTotal//{*}LineExtensionAmount", ['200.00'], "LineExtensionAmount")
        self._assert_xml_node(root, ".//{*}LegalMonetaryTotal//{*}TaxExclusiveAmount", ['200.00'], "TaxExclusiveAmount")
        self._assert_xml_node(root, ".//{*}LegalMonetaryTotal//{*}TaxInclusiveAmount", ['236.00'], "TaxInclusiveAmount")
        self._assert_xml_node(root, ".//{*}LegalMonetaryTotal//{*}PrepaidAmount", ['0.00'], "PrepaidAmount")
        self._assert_xml_node(root, ".//{*}LegalMonetaryTotal//{*}PayableAmount", ['236.00'], "PayableAmount")

        # Verificamos InvoiceLine
        self._assert_xml_node(root, ".//{*}InvoiceLine//{*}TaxTotal//{*}TaxAmount", ['18.00', '18.00', '18.00', '18.00', '0.00', '18.00'], "TaxAmount")
        self._assert_xml_node(root,".//{*}InvoiceLine//{*}TaxTotal//{*}TaxSubtotal//{*}TaxableAmount", ['100.00', '100.00', '100.00'], "TaxableAmount")
        self._assert_xml_node(root, ".//{*}InvoiceLine//{*}TaxTotal//{*}TaxSubtotal//{*}TaxAmount", ['18.00', '18.00', '18.00'], "Tax Amount")
        self._assert_xml_node(root, ".//{*}InvoiceLine//{*}TaxTotal//{*}TaxSubtotal//{*}TaxCategory//{*}Percent", ['18.0', '18.0', '18.0'], "Percent")
        self._assert_xml_node(root, ".//{*}InvoiceLine//{*}TaxTotal//{*}TaxSubtotal//{*}TaxCategory//{*}TaxExemptionReasonCode", ['10', '10', '11'], "TaxExemptionReasonCode")
        self._assert_xml_node(root, ".//{*}InvoiceLine//{*}TaxTotal//{*}TaxSubtotal//{*}TaxCategory//{*}TaxScheme//{*}ID", ['1000', '1000', '9996'], "TaxSchemeID")
        self._assert_xml_node(root, ".//{*}InvoiceLine//{*}TaxTotal//{*}TaxSubtotal//{*}TaxCategory//{*}TaxScheme//{*}Name", ['IGV', 'IGV', 'GRA'], "TaxSchemeName")
        self._assert_xml_node(root, ".//{*}InvoiceLine//{*}TaxTotal//{*}TaxSubtotal//{*}TaxCategory//{*}TaxScheme//{*}TaxTypeCode", ['VAT', 'VAT', 'FRE'], "TaxTypeCode")
        self._assert_xml_node(root, ".//{*}InvoiceLine//{*}Price//{*}PriceAmount", ['100.0', '100.0', '0.0'], "PriceAmount")

        print("--------- TEST 3 COMPLETED SUCCESSFULLY ---------")

    def test_create_invoice_withdrawal_bonus(self):
        tax_test4 = self.env['account.tax'].search(
            [('name', '=', '0% Obsequio - Retiro por bonificación')], limit=1)

        invoice_lines = [
            (0, 0, {'product_id': self.products[0].id, 'quantity': 1.0, 'price_unit': 100.0}),
            (0, 0, {'product_id': self.products[1].id, 'quantity': 1.0, 'price_unit': 100.0}),
            (0, 0, {'product_id': self.products[2].id, 'quantity': 1.0, 'price_unit': 5.0, 'tax_ids': [(4, tax_test4.id)]})
        ]

        invoice = self._create_invoice(invoice_lines)
        invoice.action_post()

        xml_content = self._get_xml_content(invoice)
        root = etree.fromstring(xml_content.decode())

        # Verificamos TaxTotal
        self._assert_xml_node(root, ".//{*}TaxTotal//{*}TaxAmount", ['36.00'], "TaxAmount")
        self._assert_xml_node(root, ".//{*}TaxTotal//{*}TaxSubtotal//{*}TaxableAmount", ['200.00', '5.00'], "TaxSubtotal TaxableAmount")
        self._assert_xml_node(root, ".//{*}TaxTotal//{*}TaxSubtotal//{*}TaxAmount", ['36.00', '0.00'], "TaxSubtotal Amount")
        self._assert_xml_node(root, ".//{*}TaxTotal//{*}TaxSubtotal//{*}TaxCategory//{*}TaxScheme//{*}ID", ['1000', '9996'], "TaxSchemeID")
        self._assert_xml_node(root, ".//{*}TaxTotal//{*}TaxSubtotal//{*}TaxCategory//{*}TaxScheme//{*}Name", ['IGV', 'GRA'], "TaxSchemeName")
        self._assert_xml_node(root, ".//{*}TaxTotal//{*}TaxSubtotal//{*}TaxCategory//{*}TaxScheme//{*}TaxTypeCode", ['VAT', 'FRE'], "TaxTypeCode")

        # Verificamos LegalMonetaryTotal
        self._assert_xml_node(root, ".//{*}LegalMonetaryTotal//{*}LineExtensionAmount", ['200.00'],"LineExtensionAmount")
        self._assert_xml_node(root, ".//{*}LegalMonetaryTotal//{*}TaxExclusiveAmount", ['200.00'], "TaxExclusiveAmount")
        self._assert_xml_node(root, ".//{*}LegalMonetaryTotal//{*}TaxInclusiveAmount", ['236.00'], "TaxInclusiveAmount")
        self._assert_xml_node(root, ".//{*}LegalMonetaryTotal//{*}PrepaidAmount", ['0.00'], "PrepaidAmount")
        self._assert_xml_node(root, ".//{*}LegalMonetaryTotal//{*}PayableAmount", ['236.00'], "PayableAmount")

        # Verificamos InvoiceLine
        self._assert_xml_node(root, ".//{*}InvoiceLine//{*}TaxTotal//{*}TaxAmount", ['18.00', '18.00', '18.00', '18.00', '0.00', '0.00'], "TaxAmount")
        self._assert_xml_node(root, ".//{*}InvoiceLine//{*}TaxTotal//{*}TaxSubtotal//{*}TaxableAmount", ['100.00', '100.00', '5.00'], "TaxableAmount")
        self._assert_xml_node(root, ".//{*}InvoiceLine//{*}TaxTotal//{*}TaxSubtotal//{*}TaxAmount", ['18.00', '18.00', '0.00'], "Tax Amount")
        self._assert_xml_node(root, ".//{*}InvoiceLine//{*}TaxTotal//{*}TaxSubtotal//{*}TaxCategory//{*}Percent", ['18.0', '18.0', '0.0'], "Percent")
        self._assert_xml_node(root, ".//{*}InvoiceLine//{*}TaxTotal//{*}TaxSubtotal//{*}TaxCategory//{*}TaxExemptionReasonCode", ['10', '10', '31'], "TaxExemptionReasonCode")
        self._assert_xml_node(root, ".//{*}InvoiceLine//{*}TaxTotal//{*}TaxSubtotal//{*}TaxCategory//{*}TaxScheme//{*}ID", ['1000', '1000', '9996'], "TaxSchemeID")
        self._assert_xml_node(root, ".//{*}InvoiceLine//{*}TaxTotal//{*}TaxSubtotal//{*}TaxCategory//{*}TaxScheme//{*}Name", ['IGV', 'IGV', 'GRA'], "TaxSchemeName")
        self._assert_xml_node(root, ".//{*}InvoiceLine//{*}TaxTotal//{*}TaxSubtotal//{*}TaxCategory//{*}TaxScheme//{*}TaxTypeCode", ['VAT', 'VAT', 'FRE'], "TaxTypeCode")
        self._assert_xml_node(root, ".//{*}InvoiceLine//{*}Price//{*}PriceAmount", ['100.0', '100.0', '0.0'], "PriceAmount")

        print("--------- TEST 4 COMPLETED SUCCESSFULLY ---------")

    def test_create_isc_tax_invoice(self):
        tax_test5 = self.env['account.tax'].create({
            'name': '30% ISC (Test)',
            'amount_type': 'percent',
            'amount': 30,
            'sequence': 1,
            'type_tax_use': 'sale',
            'l10n_pe_edi_tax_code': '2000',
            'l10n_pe_edi_unece_category': 'S',
            'l10n_pe_edi_isc_type': '01',
            'invoice_repartition_line_ids': [
                (0, 0, {
                    'repartition_type': 'base',
                    'factor_percent': 100,
                    'account_id': False,
                    'tag_ids': [(4, 19)]  # ID de la etiqueta
                }),
                (0, 0, {
                    'repartition_type': 'tax',
                    'factor_percent': 100,
                    'account_id': self.env['account.account'].search(
                        [('name', '=', 'Gobierno nacional - Impuesto selectivo al consumo')], limit=1).id
                })
            ],
            'refund_repartition_line_ids': [
                (0, 0, {
                    'repartition_type': 'base',
                    'factor_percent': 100,
                    'account_id': False,
                    'tag_ids': [(4, 18)]  # ID de la etiqueta
                }),
                (0, 0, {
                    'repartition_type': 'tax',
                    'factor_percent': 100,
                    'account_id': self.env['account.account'].search(
                        [('name', '=', 'Gobierno nacional - Impuesto selectivo al consumo')], limit=1).id
                })
            ],
        })

        self.assertEqual(tax_test5.l10n_pe_edi_isc_type, '01', "El tipo de ISC no es correcto.")

        invoice_lines = [
            (0, 0, {'product_id': self.products[0].id, 'quantity': 1.0, 'price_unit': 100.0, 'tax_ids': [(4, tax_test5.id, self.tax_18.id)]}),
            (0, 0, {'product_id': self.products[2].id, 'quantity': 1.0, 'price_unit': 100.0, 'tax_ids': [(4, self.tax_free.id)]})
        ]

        invoice = self._create_invoice(invoice_lines)
        invoice.action_post()

        xml_content = self._get_xml_content(invoice)
        root = etree.fromstring(xml_content.decode())
        print(xml_content)

        tax_exemption_reason_code = root.findall(".//{*}TaxExemptionReasonCode")
        self.assertEqual(len(tax_exemption_reason_code), 2, "deberian existir 2 etiquetas de TaxExemptionReasonCode")

        print("--------- TEST 5 COMPLETED SUCCESSFULLY ---------")

    def test_create_invoice_detraction(self):
        payment_term = self.env['account.payment.term'].create({
            'name': 'Detracción 12%, Crédito 30 y 60 días (test)',
            'early_discount': False,
            'discount_percentage': 2,
            'discount_days': 10,
            'early_pay_discount_computation': 'included',
            'line_ids': [
                (0, 0, {
                    'value_amount': 12,
                    'value': 'percent',
                    'nb_days': 1,
                    'delay_type': 'days_after',
                    'l10n_pe_is_detraction_retention': True,
                }),
                (0, 0, {
                    'value_amount': 44,
                    'value': 'percent',
                    'nb_days': 30,
                    'delay_type': 'days_after',
                    'l10n_pe_is_detraction_retention': False,
                }),
                (0, 0, {
                    'value_amount': 44,
                    'value': 'percent',
                    'nb_days': 60,
                    'delay_type': 'days_after',
                    'l10n_pe_is_detraction_retention': False,
                }),
            ],
            'display_on_invoice': True,
        })

        invoice_lines = [
            (0, 0, {'product_id': self.product_with_detraction.id, 'quantity': 1.0, 'price_unit': 1000.0, 'tax_ids': [(4, self.tax_18_ttc.id)]}),
            (0, 0, {'product_id': self.product_with_detraction.id, 'quantity': 1.0, 'price_unit': 1000.0, 'tax_ids': [(4, self.tax_18.id)]})
        ]

        invoice = self.env['account.move'].create({
            'partner_id': self.partner.id,
            'move_type': 'out_invoice',
            'l10n_pe_edi_operation_type': "1001",
            'payment_method_id': self.env['payment.methods.codes'].search([('code', '=', '003')], limit=1).id,  # transferencia de fondos
            'invoice_payment_term_id': payment_term.id,
            'invoice_line_ids': invoice_lines
        })

        invoice.action_post()
        xml_content = self._get_xml_content(invoice)
        root = etree.fromstring(xml_content.decode())

        self._assert_xml_node(root, ".//{*}PaymentMeans//{*}ID", ['Detraccion'], "PaymentMeans ID")
        self._assert_xml_node(root, ".//{*}PaymentMeans//{*}PaymentMeansCode", ['003'], "PaymentMeansCode")
        self._assert_xml_node(root, ".//{*}PaymentTerms//{*}ID", ['Detraccion', 'FormaPago', 'FormaPago', 'FormaPago'], "PaymentTerms ID")
        self._assert_xml_node(root, ".//{*}PaymentTerms//{*}PaymentMeansID", ['037', 'Credito', 'Cuota001', 'Cuota002'], "PaymentMeansCode")
        self._assert_xml_node(root, ".//{*}PaymentTerms//{*}Amount", ['262.00', '1918.40', '959.20', '959.20'], "Amount")

        self._assert_xml_node(root, ".//{*}TaxTotal//{*}TaxAmount", ['332.54'], "TaxAmount")
        self._assert_xml_node(root, ".//{*}TaxTotal//{*}TaxSubtotal//{*}TaxableAmount", ['1847.46'], "TaxSubtotal TaxableAmount")
        self._assert_xml_node(root, ".//{*}TaxTotal//{*}TaxSubtotal//{*}TaxAmount", ['332.54'], "TaxSubtotal Amount")
        self._assert_xml_node(root, ".//{*}TaxTotal//{*}TaxSubtotal//{*}TaxCategory//{*}TaxScheme//{*}ID", ['1000'], "TaxSchemeID")
        self._assert_xml_node(root, ".//{*}TaxTotal//{*}TaxSubtotal//{*}TaxCategory//{*}TaxScheme//{*}Name", ['IGV'], "TaxSchemeName")
        self._assert_xml_node(root, ".//{*}TaxTotal//{*}TaxSubtotal//{*}TaxCategory//{*}TaxScheme//{*}TaxTypeCode", ['VAT'], "TaxTypeCode")

        self._assert_xml_node(root, ".//{*}LegalMonetaryTotal//{*}LineExtensionAmount", ['1847.46'], "LineExtensionAmount")
        self._assert_xml_node(root, ".//{*}LegalMonetaryTotal//{*}TaxExclusiveAmount", ['1847.46'], "TaxExclusiveAmount")
        self._assert_xml_node(root, ".//{*}LegalMonetaryTotal//{*}TaxInclusiveAmount", ['2180.00'], "TaxInclusiveAmount")
        self._assert_xml_node(root, ".//{*}LegalMonetaryTotal//{*}PrepaidAmount", ['0.00'], "PrepaidAmount")
        self._assert_xml_node(root, ".//{*}LegalMonetaryTotal//{*}PayableAmount", ['2180.00'], "PayableAmount")

        self._assert_xml_node(root, ".//{*}InvoiceLine//{*}TaxTotal//{*}TaxAmount", ['152.54', '152.54', '180.00', '180.00'], "TaxAmount")
        self._assert_xml_node(root, ".//{*}InvoiceLine//{*}TaxTotal//{*}TaxSubtotal//{*}TaxableAmount", ['847.46', '1000.00'], "TaxableAmount")
        self._assert_xml_node(root, ".//{*}InvoiceLine//{*}TaxTotal//{*}TaxSubtotal//{*}TaxAmount", ['152.54', '180.00'], "Tax Amount")
        self._assert_xml_node(root, ".//{*}InvoiceLine//{*}TaxTotal//{*}TaxSubtotal//{*}TaxCategory//{*}Percent", ['18.0', '18.0'], "Percent")
        self._assert_xml_node(root, ".//{*}InvoiceLine//{*}TaxTotal//{*}TaxSubtotal//{*}TaxCategory//{*}TaxExemptionReasonCode", ['10', '10'], "TaxExemptionReasonCode")
        self._assert_xml_node(root, ".//{*}InvoiceLine//{*}TaxTotal//{*}TaxSubtotal//{*}TaxCategory//{*}TaxScheme//{*}ID", ['1000', '1000'], "TaxSchemeID")
        self._assert_xml_node(root, ".//{*}InvoiceLine//{*}TaxTotal//{*}TaxSubtotal//{*}TaxCategory//{*}TaxScheme//{*}Name", ['IGV', 'IGV'], "TaxSchemeName")
        self._assert_xml_node(root, ".//{*}InvoiceLine//{*}TaxTotal//{*}TaxSubtotal//{*}TaxCategory//{*}TaxScheme//{*}TaxTypeCode", ['VAT', 'VAT'], "TaxTypeCode")
        self._assert_xml_node(root, ".//{*}InvoiceLine//{*}Price//{*}PriceAmount", ['847.46', '1000.0'], "PriceAmount")

        print("--------- TEST 6 COMPLETED SUCCESSFULLY ---------")

    def test_create_invoice_detraction_2(self):
        payment_term = self.env['account.payment.term'].create({
            'name': 'Detracción 12% /saldo contado (TEST)',
            'early_discount': False,
            'discount_percentage': 2,
            'discount_days': 10,
            'early_pay_discount_computation': 'included',
            'line_ids': [
                (0, 0, {
                    'value_amount': 12,
                    'value': 'percent',
                    'nb_days': 0,
                    'delay_type': 'days_after',
                    'l10n_pe_is_detraction_retention': True,
                }),
                (0, 0, {
                    'value_amount': 88,
                    'value': 'percent',
                    'nb_days': 0,
                    'delay_type': 'days_after',
                    'l10n_pe_is_detraction_retention': False,
                })
            ],
            'display_on_invoice': True,
        })

        invoice_lines = [
            (0, 0, {'product_id': self.product_with_detraction.id, 'quantity': 1.0, 'price_unit': 999.0, 'tax_ids': [(4, self.tax_18.id)]}),
            (0, 0, {'product_id': self.product_with_detraction.id, 'quantity': 1.0, 'price_unit': 997.0, 'tax_ids': [(4, self.tax_18_ttc.id)]})
        ]

        invoice = self.env['account.move'].create({
            'partner_id': self.partner.id,
            'move_type': 'out_invoice',
            'l10n_pe_edi_operation_type': "1001",
            'payment_method_id': self.env['payment.methods.codes'].search([('code', '=', '003')], limit=1).id, #transferencia de fondos
            'invoice_payment_term_id': payment_term.id,
            'invoice_line_ids': invoice_lines
        })

        invoice.action_post()
        xml_content = self._get_xml_content(invoice)
        root = etree.fromstring(xml_content.decode())

        self._assert_xml_node(root, ".//{*}PaymentMeans//{*}ID", ['Detraccion'], "PaymentMeans ID")
        self._assert_xml_node(root, ".//{*}PaymentMeans//{*}PaymentMeansCode", ['003'], "PaymentMeansCode")
        self._assert_xml_node(root, ".//{*}PaymentTerms//{*}ID", ['Detraccion', 'FormaPago'], "PaymentTerms ID")
        self._assert_xml_node(root, ".//{*}PaymentTerms//{*}PaymentMeansID", ['037', 'Contado'], "PaymentMeansCode")
        self._assert_xml_node(root, ".//{*}PaymentTerms//{*}PaymentPercent", ['12.0'], "PaymentPercent")
        self._assert_xml_node(root, ".//{*}PaymentTerms//{*}Amount", ['261.00'], "Amount")

        self._assert_xml_node(root, ".//{*}TaxTotal//{*}TaxAmount", ['331.90'], "TaxAmount")
        self._assert_xml_node(root, ".//{*}TaxTotal//{*}TaxSubtotal//{*}TaxableAmount", ['1843.92'], "TaxSubtotal TaxableAmount")
        self._assert_xml_node(root, ".//{*}TaxTotal//{*}TaxSubtotal//{*}TaxAmount", ['331.90'], "TaxSubtotal Amount")
        self._assert_xml_node(root, ".//{*}TaxTotal//{*}TaxSubtotal//{*}TaxCategory//{*}TaxScheme//{*}ID", ['1000'], "TaxSchemeID")
        self._assert_xml_node(root, ".//{*}TaxTotal//{*}TaxSubtotal//{*}TaxCategory//{*}TaxScheme//{*}Name", ['IGV'], "TaxSchemeName")
        self._assert_xml_node(root, ".//{*}TaxTotal//{*}TaxSubtotal//{*}TaxCategory//{*}TaxScheme//{*}TaxTypeCode", ['VAT'], "TaxTypeCode")

        self._assert_xml_node(root, ".//{*}LegalMonetaryTotal//{*}LineExtensionAmount", ['1843.92'], "LineExtensionAmount")
        self._assert_xml_node(root, ".//{*}LegalMonetaryTotal//{*}TaxExclusiveAmount", ['1843.92'], "TaxExclusiveAmount")
        self._assert_xml_node(root, ".//{*}LegalMonetaryTotal//{*}TaxInclusiveAmount", ['2175.82'], "TaxInclusiveAmount")
        self._assert_xml_node(root, ".//{*}LegalMonetaryTotal//{*}PrepaidAmount", ['0.00'], "PrepaidAmount")
        self._assert_xml_node(root, ".//{*}LegalMonetaryTotal//{*}PayableAmount", ['2175.82'], "PayableAmount")

        self._assert_xml_node(root, ".//{*}InvoiceLine//{*}TaxTotal//{*}TaxAmount", ['179.82', '179.82', '152.08', '152.08'], "TaxAmount")
        self._assert_xml_node(root, ".//{*}InvoiceLine//{*}TaxTotal//{*}TaxSubtotal//{*}TaxableAmount", ['999.00', '844.92'], "TaxableAmount")
        self._assert_xml_node(root, ".//{*}InvoiceLine//{*}TaxTotal//{*}TaxSubtotal//{*}TaxAmount", ['179.82', '152.08'], "Tax Amount")
        self._assert_xml_node(root, ".//{*}InvoiceLine//{*}TaxTotal//{*}TaxSubtotal//{*}TaxCategory//{*}Percent", ['18.0', '18.0'], "Percent")
        self._assert_xml_node(root, ".//{*}InvoiceLine//{*}TaxTotal//{*}TaxSubtotal//{*}TaxCategory//{*}TaxExemptionReasonCode", ['10', '10'], "TaxExemptionReasonCode")
        self._assert_xml_node(root, ".//{*}InvoiceLine//{*}TaxTotal//{*}TaxSubtotal//{*}TaxCategory//{*}TaxScheme//{*}ID", ['1000', '1000'], "TaxSchemeID")
        self._assert_xml_node(root, ".//{*}InvoiceLine//{*}TaxTotal//{*}TaxSubtotal//{*}TaxCategory//{*}TaxScheme//{*}Name", ['IGV', 'IGV'], "TaxSchemeName")
        self._assert_xml_node(root, ".//{*}InvoiceLine//{*}TaxTotal//{*}TaxSubtotal//{*}TaxCategory//{*}TaxScheme//{*}TaxTypeCode", ['VAT', 'VAT'], "TaxTypeCode")
        self._assert_xml_node(root, ".//{*}InvoiceLine//{*}Price//{*}PriceAmount", ['999.0', '844.92'], "PriceAmount")

        print("--------- TEST 7 COMPLETED SUCCESSFULLY ---------")
