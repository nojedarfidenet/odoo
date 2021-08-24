# -*- coding: utf-8 -*-
from odoo import http

# class Cogitig(http.Controller):
#     @http.route('/cogitig/cogitig/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/cogitig/cogitig/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('cogitig.listing', {
#             'root': '/cogitig/cogitig',
#             'objects': http.request.env['cogitig.cogitig'].search([]),
#         })

#     @http.route('/cogitig/cogitig/objects/<model("cogitig.cogitig"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('cogitig.object', {
#             'object': obj
#         })