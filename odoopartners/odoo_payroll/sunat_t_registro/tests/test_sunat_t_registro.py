import unittest
import datetime
from odoo.tests.common import TransactionCase


class TestSunatRegistro(TransactionCase):

    def setUp(self):
        super(TestSunatRegistro, self).setUp()

    def test_other_annexed_establishments(self):
        other_annexed = self.env['other.annexed.establishments'].create({
            'code': '001',
            'name': 'Annexed Establishment 1',
        })

        self.assertEqual(other_annexed.code, '001')
        self.assertEqual(other_annexed.name, 'Annexed Establishment 1')
        print('---------------------------- ANNEX OK ------------------------------')

    def test_industrial_classification(self):
        industrial_classification = self.env['international.industrial.classification'].create({
            'code': '001',
            'name': 'Industrial Classification 1',
        })

        self.assertEqual(industrial_classification.code, '001')
        self.assertEqual(industrial_classification.name, 'Industrial Classification 1')

    def test_account_move(self):
        # Crear primero el establecimiento anexo
        other_annexed = self.env['other.annexed.establishments'].create({
            'code': '001',
            'name': 'Annexed Establishment 1',
        })
        partner = self.env['res.partner'].create({
            'name': 'Test Partner',
        })
        employee = self.env['hr.employee'].create({
            'name': 'Test Employee',
        })
        # Obtener el ID correcto de la clasificación industrial
        industrial_classification_id = self.env['international.industrial.classification'].search([('code', '=', '001')]).id

        account_move = self.env['hr.contract'].create({
            'name': 'contract 1',
            'displacemnent': True,
            'employer_id': partner.id,
            'date_from_displacement': datetime.date(2023, 6, 1),  # Convert string to datetime.date object
            'date_to_displacement': datetime.date(2023, 6, 30),   # Convert string to datetime.date object
            'risk_activities': True,
            'given_service': industrial_classification_id,  # Assuming the ID of the industrial classification
            'other_annexed': other_annexed.id,  # Use the ID of the created other_annexed establishment
            'employee_id': employee.id,
            'wage': 1,
        })
        print('------------------------PARTNER OK  ------------------------------')
        self.assertTrue(account_move.displacemnent)
        self.assertEqual(account_move.employer_id, partner)
        self.assertEqual(account_move.date_from_displacement, datetime.date(2023, 6, 1))  # Compare with datetime.date object
        self.assertEqual(account_move.date_to_displacement, datetime.date(2023, 6, 30))  # Compare with datetime.date object
        self.assertTrue(account_move.risk_activities)
        self.assertEqual(account_move.other_annexed, other_annexed)
        self.assertEqual(account_move.employee_id, employee)
        print('------------------------ TEST OK ------------------------------')

    def test_road_type_object(self):
        road_type = self.env['road.type.object'].create({
            'code': '001',
            'name': 'Road Type 1',
        })

        self.assertEqual(road_type.code, '001')
        self.assertEqual(road_type.name, 'Road Type 1')

    def test_zone_type_object(self):
        zone_type = self.env['zone.type.object'].create({
            'code': '001',
            'name': 'Zone Type 1',
        })

        self.assertEqual(zone_type.code, '001')
        self.assertEqual(zone_type.name, 'Zone Type 1')

    def test_ubigeo_reniec_object(self):
        ubigeo = self.env['ubigeo.reniec.object'].create({
            'code': '001',
            'name': 'Ubigeo 1',
        })

        self.assertEqual(ubigeo.code, '001')
        self.assertEqual(ubigeo.name, 'Ubigeo 1')

    def test_res_partner(self):
        road_type = self.env['road.type.object'].create({
            'code': '001',
            'name': 'Road Type 1',
        })
        zone_type = self.env['zone.type.object'].create({
            'code': '001',
            'name': 'Zone Type 1',
        })
        ubigeo = self.env['ubigeo.reniec.object'].create({
            'code': '001',
            'name': 'Ubigeo 1',
        })

        partner = self.env['res.partner'].create({
            'name': 'Test Partner',
            'road_type': road_type.id,
            'road_type_2': road_type.id,
            'zone_type': zone_type.id,
            'zone_ubigeo': ubigeo.id,
        })

        self.assertEqual(partner.name, 'Test Partner')
        self.assertEqual(partner.road_type, road_type)
        self.assertEqual(partner.road_type_2, road_type)
        self.assertEqual(partner.zone_type, zone_type)
        self.assertEqual(partner.zone_ubigeo, ubigeo)
        print('------------------------------- TEST OVER -------------------------------')
