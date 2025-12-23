# -*- coding: utf-8 -*-
import logging

from odoo.tests.common import TransactionCase


_logger = logging.getLogger(__name__)


class TestDocumentInSupplierInvoice(TransactionCase):

    def setUp(self):
        super(TestDocumentInSupplierInvoice, self).setUp()
        self.product = self.env['product.product'].create({
            'name': 'Product',
            'standard_price': 600.0,
            'list_price': 147.0,
            'detailed_type': 'consu',
        })
        self.partner_pe = self.env['res.partner'].create({
            'name': "Partner PE",
            'country_id': self.env.ref('base.pe').id,
        })

    def test_create_in_invoice(self):

        journal = self.env['account.journal'].search([
            ('code', '=', 'INV')
        ])
        l10n_latam_document_type = self.env['l10n_latam.document.type'].search([
            ('code', '=', '03'),
            ('country_id.code', '=', 'PE')
        ])
        journal.l10n_latam_use_documents = False
        l10n_latam_document_type.account_journal_id_sale = journal.id
        try:
            self.env['account.move'].create({
                'move_type': 'out_invoice',
                'date': '2024-01-01',
                'partner_id': self.partner_pe.id,
                'journal_id': journal.id,
                'l10n_latam_document_type_id': l10n_latam_document_type.id,
                'invoice_line_ids': [(0, 0, {
                    'product_id': self.product.id,
                    'price_unit': 100.0,
                    'tax_ids': [],
                })]
            })
            print('TEST CREATED SALE INVOICE OK')
        except Exception:
            _logger.error("Error when creating the invoice")
            if not journal:
                _logger.error("Journal value is empty")

    def test_create_out_invoice(self):

        journal = self.env['account.journal'].search([
            ('code', '=', 'BILL')
        ])
        if not journal:
            journal = self.env['account.journal'].search([
                ('code', '=', 'FACTU')
            ])
        l10n_latam_document_type = self.env['l10n_latam.document.type'].search([
            ('code', '=', '01'),
            ('country_id.code', '=', 'PE')
        ])
        journal.l10n_latam_use_documents = False
        l10n_latam_document_type.account_journal_id = journal.id
        try:
            self.env['account.move'].create({
                'move_type': 'in_invoice',
                'date': '2024-01-02',
                'partner_id': self.partner_pe.id,
                'journal_id': journal.id,
                'l10n_latam_document_type_id': l10n_latam_document_type.id,
                'invoice_line_ids': [(0, 0, {
                    'product_id': self.product.id,
                    'price_unit': 100.0,
                    'tax_ids': []
                })]
            })
            print('TEST CREATED PURCHASE INVOICE OK')
        except Exception:
            _logger.error("Error when creating the invoice")
            if not journal:
                _logger.error("Journal value is empty")