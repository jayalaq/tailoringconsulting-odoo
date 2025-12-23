import math
from collections import defaultdict
from datetime import datetime, timedelta

import pytz
from dateutil.relativedelta import relativedelta
from dateutil.rrule import DAILY, WEEKLY, rrule
from pytz import timezone

from odoo import models
from odoo.addons.resource.models.utils import Intervals, float_to_time
from odoo.osv import expression


class ResourceCalendar(models.Model):
    _inherit = 'resource.calendar'

    def _get_resources_day_total(self, from_datetime, to_datetime, resources=None):
        """
        @devuelve diccionario con horas de asistencia en cada día entre `from_datetime` y `to_datetime`
        """
        self.ensure_one()
        resources = self.env['resource.resource'] if not resources else resources
        resources_list = list(resources) + [self.env['resource.resource']]
        # total hours per day:  recupera asistencias con un margen de día adicional,
        # para calcular el total de horas en el primer y último día
        from_full = from_datetime - timedelta(days=1)
        to_full = to_datetime + timedelta(days=1)

        if self.env.context.get('holiday_status_id', False):
            intervals = self.with_context(holiday_status_id=True)._attendance_intervals_batch(from_full, to_full, resources=resources)
        else:
            intervals = self._attendance_intervals_batch(from_full, to_full, resources=resources)

        result = defaultdict(lambda: defaultdict(float))
        for resource in resources_list:
            day_total = result[resource.id]
            for start, stop, meta in intervals[resource.id]:
                day_total[start.date()] += (stop - start).total_seconds() / 3600
        return result

    def _attendance_intervals_batch(self, start_dt, end_dt, resources=None, domain=None, tz=None, lunch=False):
        """ Devuelve los intervalos de asistencia en el rango de fecha y hora dado.
            Los intervalos devueltos se expresan en tz especificados o en la zona horaria del recurso.
        """
        self.ensure_one()
        resources = self.env['resource.resource'] if not resources else resources
        assert start_dt.tzinfo and end_dt.tzinfo
        combine = datetime.combine
        resources_list = list(resources) + [self.env['resource.resource']]
        resource_ids = [r.id for r in resources_list]
        domain = domain if domain is not None else []
        domain = expression.AND([domain, [
            ('calendar_id', '=', self.id),
            ('resource_id', 'in', resource_ids),
            ('display_type', '=', False),
            ('day_period', '!=' if not lunch else '=', 'lunch'),
        ]])

        # para cada especificación de asistencia, genera los intervalos en el rango de fechas
        cache_dates = defaultdict(dict)
        cache_deltas = defaultdict(dict)
        result = defaultdict(list)

        calendar_attendance_model = self.env['resource.calendar.attendance']
        attendance_ids = calendar_attendance_model.search(domain)
        if self.env.context.get('holiday_status_id', False):
            days = attendance_ids.mapped('dayofweek')
            dayofweek = ['0', '1', '2', '3', '4', '5', '6']
            days_off = list(set(dayofweek) - set(days))
            days_off.sort()
            if days_off and attendance_ids and resource_ids:
                for resource_id in resource_ids:
                    if not resource_id:
                        continue
                    for off in days_off:
                        tmp_attendance = calendar_attendance_model.new({
                            'name': 'Extra ganemo',
                            'dayofweek': off,
                            'day_period': 'morning',
                            'hour_from': 0.0,
                            'hour_to': 24,
                            'calendar_id': self.id,
                            'resource_id': resource_id
                        })
                        attendance_ids += tmp_attendance
        for attendance in attendance_ids:
            for resource in resources_list:
                # expresa todas las fechas y horas en tz especificados o en la zona horaria del recurso
                tz = tz if tz else timezone((resource or self).tz)
                if (tz, start_dt) in cache_dates:
                    start = cache_dates[(tz, start_dt)]
                else:
                    start = start_dt.astimezone(pytz.utc)
                    cache_dates[(tz, start_dt)] = start
                if (tz, end_dt) in cache_dates:
                    end = cache_dates[(tz, end_dt)]
                else:
                    end = end_dt.astimezone(pytz.utc)
                    cache_dates[(tz, end_dt)] = end

                start = start.date()
                if attendance.date_from:
                    start = max(start, attendance.date_from)
                until = end.date()
                if attendance.date_to:
                    until = min(until, attendance.date_to)
                if attendance.week_type:
                    start_week_type = int(math.floor((start.toordinal() - 1) / 7) % 2)
                    if start_week_type != int(attendance.week_type):
                        # el inicio debe ser la semana de asistencia
                        # si no, se retira una semana
                        start = start + relativedelta(weeks=-1)
                weekday = int(attendance.dayofweek)

                if self.two_weeks_calendar and attendance.week_type:
                    days = rrule(WEEKLY, start, interval=2, until=until, byweekday=weekday)
                else:
                    days = rrule(DAILY, start, until=until, byweekday=weekday)

                for day in days:
                    # Las horas de asistencia se interpretan en la zona horaria del recurso
                    hour_from = attendance.hour_from
                    if (tz, day, hour_from) in cache_deltas:
                        dt0 = cache_deltas[(tz, day, hour_from)]
                    else:
                        dt0 = tz.localize(combine(day, float_to_time(hour_from)))
                        cache_deltas[(tz, day, hour_from)] = dt0

                    hour_to = attendance.hour_to
                    if (tz, day, hour_to) in cache_deltas:
                        dt1 = cache_deltas[(tz, day, hour_to)]
                    else:
                        dt1 = tz.localize(combine(day, float_to_time(hour_to)))
                        cache_deltas[(tz, day, hour_to)] = dt1
                    dt0_utc = dt0.astimezone(pytz.utc)
                    dt1_utc = dt1.astimezone(pytz.utc)
                    result[resource.id].append((max(cache_dates[(tz, start_dt)], dt0_utc), min(cache_dates[(tz, end_dt)], dt1_utc), attendance))
        return {r.id: Intervals(result[r.id]) for r in resources_list}
