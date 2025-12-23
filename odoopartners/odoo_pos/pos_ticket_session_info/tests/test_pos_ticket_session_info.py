from odoo.tests import TransactionCase
from odoo.exceptions import ValidationError
from odoo.tools import html2plaintext


class TestPosTicketSessionInfo(TransactionCase):

    def setUp(self):
        super(TestPosTicketSessionInfo, self).setUp()
        self.payment_method = self.env['pos.payment.method'].create({
            'name': 'Test Payment Method',
            'is_cash_count': True,
        })
        self.pos_config = self.env['pos.config'].create({
            'name': 'Test POS',
            'payment_method_ids': [(4, self.payment_method.id)],
        })
        self.product = self.env['product.product'].create({
            'name': 'Test Product',
            'type': 'product',
            'list_price': 100,
        })
        self.partner = self.env['res.partner'].create({'name': 'Test Customer'})
        self.employee = self.env['hr.employee'].create({'name': 'Test Employee'})
        
        # Open a new session
        self.pos_session = self.env['pos.session'].create({
            'user_id': self.env.uid,
            'config_id': self.pos_config.id,
        })

    def test_01_pos_order_change(self):
        """Test POS order change field"""
        order = self.env['pos.order'].create({
            'session_id': self.pos_session.id,
            'partner_id': self.partner.id,
            'employee_id': self.employee.id,
            'lines': [(0, 0, {
                'product_id': self.product.id,
                'qty': 1,
                'price_unit': 100,
                'price_subtotal': 100,
                'price_subtotal_incl': 100,
            })],
            'amount_total': 100,
            'amount_tax': 0,
            'amount_paid': 120,
            'amount_return': 20,
            'order_change': 20,
        })
        
        self.assertEqual(order.order_change, 20, "Order change should be 20")

    def test_02_invoice_pos_order_change(self):
        """Test invoice creation with POS order change"""
        order = self.env['pos.order'].create({
            'session_id': self.pos_session.id,
            'partner_id': self.partner.id,
            'employee_id': self.employee.id,
            'lines': [(0, 0, {
                'product_id': self.product.id,
                'qty': 1,
                'price_unit': 100,
                'price_subtotal': 100,
                'price_subtotal_incl': 100,
            })],
            'amount_total': 100,
            'amount_tax': 0,
            'amount_paid': 120,
            'amount_return': 20,
            'order_change': 20,
        })
        
        invoice_dict = order._generate_pos_order_invoice()
        invoice = self.env['account.move'].browse(invoice_dict['res_id'])
        self.assertEqual(invoice.pos_order_change, 20, "Invoice POS order change should be 20")

    def test_03_payment_info_on_invoice_report(self):
        """Test payment info on invoice report"""
        order = self.env['pos.order'].create({
            'session_id': self.pos_session.id,
            'partner_id': self.partner.id,
            'employee_id': self.employee.id,
            'lines': [(0, 0, {
                'product_id': self.product.id,
                'qty': 1,
                'price_unit': 100,
                'price_subtotal': 100,
                'price_subtotal_incl': 100,
            })],
            'amount_total': 100,
            'amount_tax': 0,
            'amount_paid': 120,
            'amount_return': 20,
            'order_change': 20,
        })
        
        self.env['pos.payment'].create({
            'pos_order_id': order.id,
            'payment_method_id': self.payment_method.id,
            'amount': 120,
        })
        
        invoice_dict = order._generate_pos_order_invoice()
        invoice = self.env['account.move'].browse(invoice_dict['res_id'])
        report = self.env['ir.actions.report']._get_report_from_name('account.report_invoice')
        html = report._render_qweb_html('account.report_invoice_with_payments',docids=[invoice.id])[0].decode('utf-8')
        text = html2plaintext(html)
        self.assertIn('B 00000003', text)

    def test_04_session_info_on_invoice_report(self):
        """Test session info on invoice report"""
        order = self.env['pos.order'].create({
            'session_id': self.pos_session.id,
            'partner_id': self.partner.id,
            'employee_id': self.employee.id,
            'lines': [(0, 0, {
                'product_id': self.product.id,
                'qty': 1,
                'price_unit': 100,
                'price_subtotal': 100,
                'price_subtotal_incl': 100,
            })],
            'amount_total': 100,
            'amount_tax': 0,
            'amount_paid': 100,
            'amount_return': 0,
        })
        
        invoice_dict = order._generate_pos_order_invoice()
        invoice = self.env['account.move'].browse(invoice_dict['res_id'])
        report = self.env['ir.actions.report']._get_report_from_name('account.report_invoice')
        html = report._render_qweb_html('account.report_invoice_with_payments',docids=[invoice.id])[0].decode('utf-8')
        text = html2plaintext(html)
        self.assertIn('B 00000003', text)

    
        
    
