
from odoo.tests import common,tagged
import logging
from datetime import date

_logger = logging.getLogger(__name__)

@tagged('-at_install', 'post_install')
class TestBankMassivePayment(common.TransactionCase):
    def setUp(self):
        super().setUp()
        # Crear datos necesarios para el test
        self.partner_bank = self.env['res.partner'].create({
            'name': 'Partner Bank'
        })
        self.res_bank = self.env['res.bank'].create({
            'name':'Banco de la Nacion',
            'bic':'BANCPEPL',
            'country':self.env['res.country'].search([('name','=','Peru')]).id,
            'sunat_bank_code': '01'
        })
        self.bank_account = self.env['res.partner.bank'].create({
            'acc_number': '513132132321',
            'acc_holder_name':'232323223',
            'acc_type':'cts',
            'partner_id': self.partner_bank.id,
            'bank_id': self.res_bank.id, 
            'type_bank_code':'02',
            'cci':'65413132131231',
            'currency_id':self.env['res.currency'].search([('name','=','PEN')]).id
        })
        self.test_employee = self.env['hr.employee'].create({
            'name': 'Test User - employee',
            'user_id': self.env['res.users'].search([])[0].id,
            'company_id': self.env['res.company'].search([])[0].id,
            'bank_account_id': self.bank_account.id,
        })
        self.payslip = self.env['hr.payslip'].create({
            'name': 'Test Payslip',
            'employee_id': self.test_employee.id,
            'date_from': date.today(),
            'date_to': date.today(),
        })
        
    def test_generate_massive_payment(self):
        massive_payment = self.env['hr.massive.payment'].create({
            'payment_date': date.today(),
            'acc_type': 'cts',
            'exchange_type': 1.0,
            'partner_id': self.partner_bank.id,
            'payment_type_id': self.bank_account.id,
            'is_validate_account': False,
            'payslip_ids': [(6, 0, [self.payslip.id])]
        })
        
        self.assertEqual(massive_payment.payment_date, date.today())    
        self.assertEqual(massive_payment.acc_type,'cts')    
        self.assertEqual(massive_payment.exchange_type,1.0)    
        self.assertEqual(massive_payment.partner_id.id,self.partner_bank.id)    
        self.assertEqual(massive_payment.payment_type_id.id,self.bank_account.id)  
        self.assertEqual(self.res_bank.sunat_bank_code,'01')  
        self.assertFalse(massive_payment.txt_filename)
        # Boton de Generar Archvio
        massive_payment.generate_files()
        self.assertTrue(massive_payment)
        self.assertTrue(massive_payment.txt_filename,'Error the generate file')
        _logger.info("File generate successfully")