# -*- coding: utf-8 -*-
from odoo import http

# class PTask(http.Controller):
#     @http.route('/p_task/p_task/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/p_task/p_task/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('p_task.listing', {
#             'root': '/p_task/p_task',
#             'objects': http.request.env['p_task.p_task'].search([]),
#         })

#     @http.route('/p_task/p_task/objects/<model("p_task.p_task"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('p_task.object', {
#             'object': obj
#         })