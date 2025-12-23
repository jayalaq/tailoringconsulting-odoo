from odoo import fields
from odoo.tests import common

class TestPosSerieCorrelativePle(common.TransactionCase):
    def setUp(self):
        super(TestPosSerieCorrelativePle, self).setUp()
        
        self.document_type = self.env['l10n_latam.document.type'].create({
            'name': 'Factura',
            'code': '01',
            'country_id': self.env.ref('base.pe').id
        })
        self.pos_session = self.env['pos.session'].create({
            'name': 'Test Session',
            'state': 'opened',
            'config_id': self.env.ref('point_of_sale.pos_config_main').id,
            'start_at': fields.Datetime.now(),
        })

    def test_computed_fields(self):
        pos_order = self.env['pos.order'].create({
            'partner_id': self.env.ref('base.res_partner_1').id,
            'session_id': self.pos_session.id, 
            'amount_total': 100.0,
            'amount_tax': 0.0,
            'amount_paid': 100.0,
            'amount_return': 0.0,
        })
        invoice = self.env['account.move'].create({
            'partner_id': self.env.ref('base.res_partner_1').id,
            'move_type': 'out_invoice',
            'name': 'F001-00000001',
            'l10n_latam_document_type_id': self.document_type.id
        })
        pos_order.write({
            'account_move': invoice.id
        })
        # Crear un picking y vincularlo a la orden POS
        picking = self.env['stock.picking'].create({
            'partner_id': self.env.ref('base.res_partner_1').id,
            'picking_type_id': self.env.ref('stock.picking_type_out').id,
            'location_id': self.env.ref('stock.stock_location_stock').id,
            'location_dest_id': self.env.ref('stock.stock_location_customers').id,
            'pos_order_id': pos_order.id
        })

        # Forzar el cálculo de los datos de transferencia
        picking._compute_transfer_data_picking()

        # Aserciones
        self.assertEqual(picking.serie_transfer_document, 'F001', 
                        "Serie del documento de transferencia no coincide")
        self.assertEqual(picking.number_transfer_document, '00000001', 
                        "Número del documento de transferencia no coincide")
        self.assertEqual(picking.transfer_document_type_id, self.document_type, 
                        "Tipo de documento de transferencia no coincide")

        print('------------------------ TEST OK--------------------------')
