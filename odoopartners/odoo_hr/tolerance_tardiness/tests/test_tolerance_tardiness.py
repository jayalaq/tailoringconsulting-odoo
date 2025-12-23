import math
from datetime import datetime

from odoo import fields
from odoo.tests import common


@common.tagged('post_install', '-at_install')
class TestToleranceTardiness(common.TransactionCase):

    def setUp(self):
        super().setUp()
        self.attendance = self.env['hr.attendance']
        self.calendar = self.env['resource.calendar'].create({
            'name': 'Calendario de Prueba',
            'attendance_ids': [
                (0, 0, {'name': 'Lunes en la mañana', 'dayofweek': '0', 'hour_from': 8, 'hour_to': 12, 'day_period': 'morning'}),
                (0, 0, {'name': 'Almuerzo del lunes', 'dayofweek': '0', 'hour_from': 12, 'hour_to': 13, 'day_period': 'lunch'}),
                (0, 0, {'name': 'Lunes en la tarde', 'dayofweek': '0', 'hour_from': 13, 'hour_to': 17, 'day_period': 'afternoon'}),
                (0, 0, {'name': 'Martes en la mañana', 'dayofweek': '1', 'hour_from': 8, 'hour_to': 12, 'day_period': 'morning'}),
                (0, 0, {'name': 'Almuerzo del martes', 'dayofweek': '1', 'hour_from': 12, 'hour_to': 13, 'day_period': 'lunch'}),
                (0, 0, {'name': 'Martes en la tarde', 'dayofweek': '1', 'hour_from': 13, 'hour_to': 17, 'day_period': 'afternoon'}),
                (0, 0, {'name': 'Miercoles en la mañana', 'dayofweek': '2', 'hour_from': 8, 'hour_to': 12, 'day_period': 'morning'}),
                (0, 0, {'name': 'Almuerzo del miercoles', 'dayofweek': '2', 'hour_from': 12, 'hour_to': 13, 'day_period': 'lunch'}),
                (0, 0, {'name': 'Miercoles en la tarde', 'dayofweek': '2', 'hour_from': 13, 'hour_to': 17, 'day_period': 'afternoon'}),
                (0, 0, {'name': 'Jueves en la mañana', 'dayofweek': '3', 'hour_from': 8, 'hour_to': 12, 'day_period': 'morning'}),
                (0, 0, {'name': 'Almuerzo del jueves', 'dayofweek': '3', 'hour_from': 12, 'hour_to': 13, 'day_period': 'lunch'}),
                (0, 0, {'name': 'Jueves en la tarde', 'dayofweek': '3', 'hour_from': 13, 'hour_to': 17, 'day_period': 'afternoon'}),
                (0, 0, {'name': 'Viernes en la mañana', 'dayofweek': '4', 'hour_from': 8, 'hour_to': 12, 'day_period': 'morning'}),
                (0, 0, {'name': 'Almuerzo del viernes', 'dayofweek': '4', 'hour_from': 12, 'hour_to': 13, 'day_period': 'lunch'}),
                (0, 0, {'name': 'Viernes en la tarde', 'dayofweek': '4', 'hour_from': 13, 'hour_to': 17, 'day_period': 'afternoon'})
            ],
            'two_weeks_calendar': False
        })
        self.employee = self.env['hr.employee'].create({
            'name': 'Empleado de Prueba',
            'resource_calendar_id': self.calendar.id
        })

    def test_calculate_tardiness(self):
        # Caso 1: Tardanza dentro de la tolerancia
        check_in_time_1 = '2023-12-25 08:15:00'
        check_out_time_1 = '2023-12-25 12:00:00'
        expected_tardiness_1 = False

        # Caso 2: Tardanza excede la tolerancia
        check_in_time_2 = '2023-12-26 08:25:00'
        check_out_time_2 = '2023-12-26 12:00:00'
        expected_tardiness_2 = '10 minuto(s)'

        # Configurar calendario con tolerancia
        self.calendar.write({'tolerance_time': 15})

        # Prueba Caso 1
        attendance_1 = self.attendance.create({
            'check_in': check_in_time_1,
            'check_out': check_out_time_1,
            'employee_id': self.employee.id,
        })
        self.assertEqual(attendance_1.tardiness, expected_tardiness_1)
        
        # Prueba Caso 2
        attendance_2 = self.attendance.create({
            'check_in': check_in_time_2,
            'check_out': check_out_time_2,
            'employee_id': self.employee.id,
        })
        self.assertEqual(attendance_2.tardiness, expected_tardiness_2)

    def test_convert_date_to_user_timezone(self):
        # Caso 3: Convertir fecha a la zona horaria del usuario
        input_date = '2023-01-01 08:30:00'
        expected_output_date = '2023-01-01 11:30:00'  # Suponiendo que la zona horaria del usuario es UTC+3

        user_timezone = 'Etc/GMT-3'
        self.env.user.tz = user_timezone

        converted_date = self.attendance._convert_date_to_user_timezone(input_date)
        expected_output_date = datetime.strptime(expected_output_date, '%Y-%m-%d %H:%M:%S')
        self.assertEqual(converted_date, expected_output_date)

    def test_get_calendar_attendance(self):
        # Caso 4: Asistencia del calendario para la semana normal, mañana
        expected_attendance_1 = self.calendar.attendance_ids.filtered(
            lambda x: x.dayofweek == '0' and x.day_period == 'morning'
        )

        # Prueba Caso 4
        result_attendance_1 = self.attendance._get_calendar_attendance(self.calendar, '0')
        self.assertEqual(result_attendance_1, expected_attendance_1)
        
        # Caso 5: Asistencia del calendario para semana par o impar, mañana
        self.calendar.switch_calendar_type()
        date_today = fields.Date.today()
        week_type = '1' if int(math.floor((date_today.toordinal() - 1) / 7) % 2) else '0'
        expected_attendance_2 = self.calendar.attendance_ids.filtered(
            lambda attendance: attendance.dayofweek == '0'
            and attendance.day_period == 'morning'
            and attendance.week_type == week_type
            and attendance.display_type != 'line_section'
        )

        # Prueba Caso 5
        result_attendance_2 = self.attendance._get_calendar_attendance(self.calendar, '0')
        self.assertEqual(result_attendance_2, expected_attendance_2)

    def test_calculate_minutes_minimum_allowed_arrival(self):
        # Caso 6: Calcular minutos de llegada mínima permitida para hour_from > 1
        hour_from = 9.25
        tolerance_time = 15
        expected_result = (int(hour_from) * 60) + int((hour_from - int(hour_from)) * 100) + tolerance_time

        # Prueba Caso 6
        result = self.attendance._calculate_minutes_minimum_allowed_arrival(hour_from, tolerance_time)
        self.assertEqual(result, expected_result)

        # Caso 7: Calcular minutos de llegada mínima permitida para hour_from <= 1
        hour_from = 0.75
        tolerance_time = 10
        expected_result = int((hour_from - int(hour_from)) * 100) + tolerance_time

        # Prueba Caso 7
        result = self.attendance._calculate_minutes_minimum_allowed_arrival(hour_from, tolerance_time)
        self.assertEqual(result, expected_result)

        # Caso 8: Calcular minutos de llegada mínima permitida para hour_from <= 1 y tolerance_time = 0
        hour_from = 0.75
        tolerance_time = 0
        expected_result = int((hour_from - int(hour_from)) * 100)

        # Prueba Caso 8
        result = self.attendance._calculate_minutes_minimum_allowed_arrival(hour_from, tolerance_time)
        self.assertEqual(result, expected_result)
