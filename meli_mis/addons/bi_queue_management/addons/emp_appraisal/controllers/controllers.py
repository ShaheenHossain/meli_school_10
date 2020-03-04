# -*- coding: utf-8 -*-
from odoo import http

# class EmpAppraisal(http.Controller):
#     @http.route('/emp_appraisal/emp_appraisal/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/emp_appraisal/emp_appraisal/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('emp_appraisal.listing', {
#             'root': '/emp_appraisal/emp_appraisal',
#             'objects': http.request.env['emp_appraisal.emp_appraisal'].search([]),
#         })

#     @http.route('/emp_appraisal/emp_appraisal/objects/<model("emp_appraisal.emp_appraisal"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('emp_appraisal.object', {
#             'object': obj
#         })