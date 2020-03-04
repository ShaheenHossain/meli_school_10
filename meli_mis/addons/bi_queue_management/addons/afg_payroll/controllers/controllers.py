# -*- coding: utf-8 -*-
from odoo import http

# class AfgPayroll(http.Controller):
#     @http.route('/afg_payroll/afg_payroll/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/afg_payroll/afg_payroll/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('afg_payroll.listing', {
#             'root': '/afg_payroll/afg_payroll',
#             'objects': http.request.env['afg_payroll.afg_payroll'].search([]),
#         })

#     @http.route('/afg_payroll/afg_payroll/objects/<model("afg_payroll.afg_payroll"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('afg_payroll.object', {
#             'object': obj
#         })