# -*- coding: utf-8 -*-

import math
from datetime import datetime, time
from odoo import tools
from odoo import api, fields, models
from odoo.tools import float_round
from pytz import timezone, utc
import logging
log = logging.getLogger(__name__)


def float_to_time(hours):
    """ Convert a number of hours into a time object. """
    if hours == 24.0:
        return time.max
    fractional, integral = math.modf(hours)
    return time(int(integral), int(float_round(60 * fractional, precision_digits=0)), 0)


class HrScheduleCal(models.Model):
    _name = 'hr.schedule.cal'
    _auto = False
    _description = 'Horario de Empleados'
    _order = 'fecha_inicio desc'
    _rec_name = 'fecha_inicio'

    employee_id = fields.Many2one('hr.employee', string="Empleado", readonly=True)
    fecha_inicio = fields.Datetime(string='Entrada', compute='_hora_entrada', readonly=True)
    fecha = fields.Date(string='Fecha', readonly=True)
    hora = fields.Float(string='Hora', readonly=True)
    duracion = fields.Float(string='Duracion', readonly=True)

    def convert_timezone_utc(self, fecha):
        now_utc = datetime.now(timezone('UTC'))
        if self.env.user.tz:
            now_timezone = now_utc.astimezone(timezone(self.env.user.tz))
        else:
            now_timezone = now_utc.astimezone(timezone('UTC'))
        utc_offset_timedelta = datetime.strptime(now_utc.strftime("%Y-%m-%d %H:%M:%S"),
                                                 "%Y-%m-%d %H:%M:%S") - datetime.strptime(
            now_timezone.strftime("%Y-%m-%d %H:%M:%S"), "%Y-%m-%d %H:%M:%S")
        local_datetime = datetime.strptime(fecha, "%Y-%m-%d %H:%M:%S")
        utc_datetime = local_datetime + utc_offset_timedelta
        return utc_datetime.strftime("%Y-%m-%d %H:%M:%S")

    @api.depends('fecha', 'hora')
    def _hora_entrada(self):
        for r in self:
            fecha_inicio = (datetime.combine(r.fecha, float_to_time(r.hora)))
            r.fecha_inicio = self.convert_timezone_utc(str(fecha_inicio))

    def _select(self):
        select_str = """
        SELECT row_number() OVER ()::integer AS id
        , my_query.x_fecha_ini AS fecha
        , my_query.x_hora AS hora
        , my_query.x_duracion AS duracion
        , my_query.x_nombre AS employee_id
        """
        return select_str

    def _from(self):
        from_str = """
        (SELECT DISTINCT generate_series(rca.date_from, rca.date_to, '1 day'::interval)::date           AS x_fecha_ini,
                      rca.hour_from                                                                     AS x_hora,
                      rca.hour_to - rca.hour_from                                                       AS x_duracion,
                      e.id                                                                              AS x_nombre
        FROM hr_employee e
          JOIN resource_resource rr ON e.resource_id = rr.id
          JOIN resource_calendar_attendance rca ON rr.calendar_id = rca.calendar_id) my_query
        """
        return from_str

    @api.model_cr
    def init(self):
        tools.drop_view_if_exists(self.env.cr, self._table)
        query = """
            CREATE OR REPLACE VIEW %s AS (
                %s
                FROM
                %s)
            """ % (self._table, self._select(), self._from())
        self.env.cr.execute(query)
