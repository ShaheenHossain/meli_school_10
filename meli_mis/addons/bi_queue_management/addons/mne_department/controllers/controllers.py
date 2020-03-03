# -*- coding: utf-8 -*-
from odoo import http

# class MneDepartment(http.Controller):
#     @http.route('/mne_department/mne_department/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/mne_department/mne_department/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('mne_department.listing', {
#             'root': '/mne_department/mne_department',
#             'objects': http.request.env['mne_department.mne_department'].search([]),
#         })

#     @http.route('/mne_department/mne_department/objects/<model("mne_department.mne_department"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('mne_department.object', {
#             'object': obj
#         })