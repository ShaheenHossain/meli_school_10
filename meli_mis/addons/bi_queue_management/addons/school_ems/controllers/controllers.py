# -*- coding: utf-8 -*-
from odoo import http

# class SchoolEms(http.Controller):
#     @http.route('/school_ems/school_ems/', type='http', auth='public', website=True)
#     def index(self, **kw):
#          return http.request.render('school_ems.example_page11', {})

#     @http.route('/school_ems/school_ems/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('school_ems.listing', {
#             'root': '/school_ems/school_ems',
#             'objects': http.request.env['school_ems.school_ems'].search([]),
#         })

#     @http.route('/school_ems/school_ems/objects/<model("school_ems.school_ems"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('school_ems.object', {
#             'object': obj
#         })


class ExampleView(http.Controller):
    @http.route('/example', type='http', auth='public', website=True)
    def render_demo_page(self):
        return http.request.render('school_ems.example_page11', {})



    @http.route('/example/detail', type='http', auth='public', website=True)
    def navigate_to_detail_page(self):
    	students= http.request.env['student.student'].sudo().search([])
        return http.request.render('school_ems.detail_page222', {'students':students})


    @http.route('/example/campus', type='http', auth='public', website=True)
    def navigate_to_detail_page11(self):
    	campuses= http.request.env['school.school'].sudo().search([])
        return http.request.render('school_ems.campus_list', {'student':campuses})

