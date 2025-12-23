from odoo.tests.common import TransactionCase


class TestAccountJournal(TransactionCase):
    """
    Pruebas unitarias para la clase AccountJournal.
    Verifica la correcta herencia y adición de campos personalizados.
    """

    def test_bank_id_related(self):
        """Prueba que el campo 'bank_id_related' se asigna correctamente."""
        journal = self.env['account.journal'].create({
            'name': 'Test Journal',
            'type': 'bank',
            'bank_id': self.env['res.bank'].create({
                'name': 'Test Bank',
                'sunat_bank_code': '11'
            }).id,
        })
        self.assertEqual(journal.bank_id_related, '11', 'El código de banco relacionado no se asignó correctamente.')


class TestResPartnerBank(TransactionCase):
    """
    Pruebas unitarias para la clase ResPartnerBank.
    Verifica la correcta herencia y adición de campos personalizados.
    """

    def test_account_type(self):
        """Prueba que el campo 'account_type' se asigna correctamente."""
        partner = self.env['res.partner'].create({
            'name': 'Test Partner',
        })
        bank_account = self.env['res.partner.bank'].create({
            'partner_id': partner.id,
            'acc_number': '1234567890',
            'bank_id': self.env['res.bank'].create({'name': 'Test Bank'}).id,
            'account_type': '001',
        })
        self.assertEqual(bank_account.account_type, '001', 'El tipo de cuenta no se asignó correctamente.')


class TestAccountBatchPayment(TransactionCase):
    """
    Pruebas unitarias para la clase AccountBatchPayment.
    Verifica la correcta herencia y adición de campos personalizados, así como la lógica del método 'generate_txt_suppliers'.
    """

    def setUp(self):
        super(TestAccountBatchPayment, self).setUp()

        self.company = self.env.ref('base.main_company')

        self.partner = self.env['res.partner'].create({
            'name': 'Test Partner',
            'l10n_latam_identification_type_id': self.env.ref('l10n_latam_base.it_vat').id,
            'vat': '123456789',
            'company_id': self.company.id,
        })

        self.bank = self.env['res.bank'].create({'name': 'Test Bank', 'sunat_bank_code': '11'})

        self.bank_account = self.env['res.partner.bank'].create({
            'acc_number': '123456789',
            'partner_id': self.company.partner_id.id,
            'bank_id': self.bank.id,
            'company_id': self.company.id,
        })

        self.journal = self.env['account.journal'].create({
            'name': 'Test Journal',
            'type': 'bank',
            'bank_id': self.bank.id,
            'bank_account_id': self.bank_account.id,
            'company_id': self.company.id,
        })

        self.payment = self.env['account.payment'].create({
            'payment_type': 'outbound',
            'partner_type': 'supplier',
            'partner_id': self.partner.id,
            'amount': 1000.0,
            'payment_method_id': self.env.ref('account.account_payment_method_manual_out').id,
            'journal_id': self.journal.id,
            'company_id': self.company.id,
        })
        self.payment.action_post()        

        self.batch_payment = self.env['account.batch.payment'].create({
            'journal_id': self.journal.id,
            'payment_ids': [(6, 0, [self.payment.id])],
            'batch_type': 'outbound',
        })
        self.batch_payment.validate_batch()

    def test_generate_txt_suppliers_bbva(self):
        """
        Prueba la generación del archivo TXT para pagos de proveedores del banco BBVA.
        """
        self.journal.bank_id_related = '11'  # BBVA
        self.batch_payment.generate_txt_suppliers()
        self.assertTrue(self.batch_payment.txt_binary_bank, 'No se generó el archivo TXT para BBVA')
        self.assertTrue(self.batch_payment.txt_filename_bank, 'No se generó el nombre del archivo para BBVA')

    def test_generate_txt_suppliers_bcp(self):
        """
        Prueba la generación del archivo TXT para pagos de proveedores del banco BCP.
        """
        self.journal.bank_id_related = '02'  # BCP
        self.batch_payment.generate_txt_suppliers()
        self.assertTrue(self.batch_payment.txt_binary_bank, 'No se generó el archivo TXT para BCP')
        self.assertTrue(self.batch_payment.txt_filename_bank, 'No se generó el nombre del archivo para BCP')

    def test_generate_txt_suppliers_interbank(self):
        """
        Prueba la generación del archivo TXT para pagos de proveedores del banco Interbank.
        """
        self.journal.bank_id_related = '03'  # Interbank
        self.journal.company_code = 'TEST'
        self.journal.service_code = 'SRV'
        self.batch_payment.generate_txt_suppliers()
        self.assertTrue(self.batch_payment.txt_binary_bank, 'No se generó el archivo TXT para Interbank')
        self.assertTrue(self.batch_payment.txt_filename_bank, 'No se generó el nombre del archivo para Interbank')

# ./opt/odoo_dir/odoo/odoo-bin -i pago_masivo_proveedores --log-level=test -d ganemo-prueba -c /etc/odoo/odoo.conf --test-enable --stop-after-init
