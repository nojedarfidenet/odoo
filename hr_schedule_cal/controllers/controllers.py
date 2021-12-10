# -*- coding: utf-8 -*-
from odoo import http

# class HrScheduleCal(http.Controller):
#     @http.route('/hr_schedule_cal/hr_schedule_cal/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/hr_schedule_cal/hr_schedule_cal/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('hr_schedule_cal.listing', {
#             'root': '/hr_schedule_cal/hr_schedule_cal',
#             'objects': http.request.env['hr_schedule_cal.hr_schedule_cal'].search([]),
#         })

#     @http.route('/hr_schedule_cal/hr_schedule_cal/objects/<model("hr_schedule_cal.hr_schedule_cal"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('hr_schedule_cal.object', {
#             'object': obj
#         })