import math
from datetime import datetime

import pytz
from odoo import api, fields, models
from odoo.exceptions import ValidationError


class HrAttendance(models.Model):
    _inherit = 'hr.attendance'

    tardiness = fields.Char(
        string='Tardanza',
        readonly=True
    )

    def _calculate_tardiness(self, check_in, employee_id):
        """
        Calcula la tardanza de un empleado basándose en su hora de entrada y su horario laboral.

        :param check_in: La hora de entrada del empleado.
        :type check_in: str
        :param employee_id: ID del empleado.
        :type employee_id: int
        :return: La tardanza en formato de cadena o False si no hay tardanza.
        :rtype: str or False
        """
        employee = self.env['hr.employee'].browse(employee_id)
        converted_check_in = self._convert_date_to_user_timezone(check_in)
        calendar = employee.resource_calendar_id
        index_dayofweek = str(converted_check_in.weekday())

        calendar_attendance = self._get_calendar_attendance(calendar, index_dayofweek)

        if len(calendar_attendance) > 1:
            raise ValidationError(
                'En la jornada laboral seteada en su ficha de empleado, '
                'tiene horarios que se traslapan en el mismo día, '
                'primero debe corregirlo.'
            )
        elif len(calendar_attendance) == 0:
            raise ValidationError(
                'En la jornada laboral seteada en su ficha de empleado, '
                'no tiene horario para el día de hoy.'
            )

        hour_from = calendar_attendance.hour_from if calendar_attendance else False
        if converted_check_in and hour_from:
            tolerance_time = calendar.tolerance_time
            minutes_minimum_allowed_arrival = self._calculate_minutes_minimum_allowed_arrival(hour_from, tolerance_time)
            minutes_check_in = (int(converted_check_in.hour) * 60) + int(converted_check_in.minute)

            if minutes_check_in > minutes_minimum_allowed_arrival:
                minutes_tardiness = minutes_check_in - minutes_minimum_allowed_arrival

                if minutes_tardiness < 60:
                    return f'{minutes_tardiness} minuto(s)'

                hours_tardiness, minute_tardiness = divmod(minutes_tardiness, 60)
                return f'{hours_tardiness} hora(s) {minute_tardiness} minuto(s)'

        return False

    def _convert_date_to_user_timezone(self, input_date, date_format='%Y-%m-%d %H:%M:%S'):
        """
        Convierte la fecha dada a la zona horaria del usuario actual en Odoo.

        :param input_date: La fecha a convertir, puede ser una cadena o un objeto datetime.
        :type input_date: str or datetime.datetime
        :param date_format: El formato de la cadena de fecha si `input_date` es una cadena.
                            Por defecto: '%Y-%m-%d %H:%M:%S'.
        :type date_format: str
        :return: La fecha convertida a la zona horaria del usuario.
        :rtype: datetime.datetime
        """
        user_timezone = pytz.timezone(self.env.user.tz) if self.env.user.tz else pytz.utc

        if isinstance(input_date, str):
            input_date = datetime.strptime(input_date, date_format)

        if input_date:
            converted_date = pytz.utc.localize(input_date).astimezone(user_timezone)
            formatted_date = converted_date.strftime(date_format)
            final_date = datetime.strptime(formatted_date, date_format)
            return final_date
        else:
            return input_date

    @api.model
    def _get_calendar_attendance(self, calendar, index_dayofweek):
        """
        Obtiene la línea de horario correspondiente al día y tipo de semana dados.

        :param calendar: El horario laboral del empleado.
        :type calendar: resource.calendar
        :param index_dayofweek: El índice del día de la semana (0=lunes, 1=martes, ..., 6=domingo).
        :type index_dayofweek: str
        :return: La línea de horario correspondiente o una lista vacía si no se encuentra.
        :rtype: resource.calendar.attendance
        """
        filter_conditions = [
            lambda attendance: attendance.dayofweek == index_dayofweek
            and attendance.day_period == 'morning'
        ]

        if calendar.two_weeks_calendar:
            date_today = fields.Date.today()
            week_type = '1' if int(math.floor((date_today.toordinal() - 1) / 7) % 2) else '0'
            filter_conditions.extend([
                lambda attendance: attendance.week_type == week_type,
                lambda attendance: attendance.display_type != 'line_section'
            ])

        calendar_attendance = calendar.attendance_ids.filtered(
            lambda attendance: all(condition(attendance) for condition in filter_conditions)
        )
        return calendar_attendance

    @api.model
    def _calculate_minutes_minimum_allowed_arrival(self, hour_from, tolerance_time):
        """
        Calcula el tiempo mínimo permitido de llegada en minutos basándose en la hora de inicio y la tolerancia.

        :param hour_from: La hora de inicio del horario laboral.
        :type hour_from: float
        :param tolerance_time: La tolerancia en minutos.
        :type tolerance_time: int
        :return: El tiempo mínimo permitido de llegada en minutos.
        :rtype: int
        """
        if int(hour_from) > 1:
            return (int(hour_from) * 60) + int((hour_from - int(hour_from)) * 100) + tolerance_time
        else:
            return int((hour_from - int(hour_from)) * 100) + tolerance_time

    @api.model_create_multi
    def create(self, values):
        for value in values:
            if value.get('check_in') and value.get('employee_id'):
                value['tardiness'] = self._calculate_tardiness(value['check_in'], value['employee_id'])
        return super().create(values)

    def write(self, values):
        for rec in self:
            if values.get('check_in') and values.get('employee_id'):
                values['tardiness'] = self._calculate_tardiness(values['check_in'], values['employee_id'])
            elif values.get('check_in') and not values.get('employee_id'):
                values['tardiness'] = self._calculate_tardiness(values['check_in'], rec.employee_id.id)
            elif not values.get('check_in') and values.get('employee_id'):
                values['tardiness'] = self._calculate_tardiness(rec.check_in, values['employee_id'])
        return super().write(values)
