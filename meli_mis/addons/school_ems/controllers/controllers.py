

# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request
class PartnerForm(http.Controller):
    #mention class name
    @http.route(['/customer/form'], type='http', auth="public", website=True)
   
    def partner_form(self, **post):
        return request.render("school_ems.tmp_customer_form", {})
        
    @http.route(['/customer/form/submit'], type='http', auth="public", website=True)
    def customer_form_submit(self, **post):
        partner = request.env['website.support.ticket'].create({
            'name': post.get('f_name'),
            'last_name': post.get('f_name'),
            'mobile': post.get('p_number'),
            'email': post.get('email'),
            'message': post.get('about'),
            
        })

        vals = {
            'partner': partner,
        }
        

        #inherited the model to pass the values to the model from the form#













# # -*- coding: utf-8 -*-
# from odoo import http

# # class SchoolEms(http.Controller):
# #     @http.route('/school_ems/school_ems/', type='http', auth='public', website=True)
# #     def index(self, **kw):
# #          return http.request.render('school_ems.example_page11', {})

# #     @http.route('/school_ems/school_ems/objects/', auth='public')
# #     def list(self, **kw):
# #         return http.request.render('school_ems.listing', {
# #             'root': '/school_ems/school_ems',
# #             'objects': http.request.env['school_ems.school_ems'].search([]),
# #         })

# #     @http.route('/school_ems/school_ems/objects/<model("school_ems.school_ems"):obj>/', auth='public')
# #     def object(self, obj, **kw):
# #         return http.request.render('school_ems.object', {
# #             'object': obj
# #         })


# class ExampleView(http.Controller):
#     @http.route('/example', type='http', auth='public', website=True)
#     def render_demo_page(self):
#         return http.request.render('school_ems.example_page11', {})



#     @http.route('/example/detail', type='http', auth='public', website=True)
#     def navigate_to_detail_page(self):
#     	students= http.request.env['student.student'].sudo().search([])
#         return http.request.render('school_ems.detail_page222', {'students':students})


#     # @http.route('/example/campus', type='http', auth='public', website=True)
#     # def navigate_to_detail_page11(self):
# class MyController(http.Controller):
#     @http.route('/api/save', auth='public', methods=['POST'],website=True, csrf=False)
#     def save_obj(self, **kw):
#         print "4444444444444444444444444"
#         obj = json.loads(kw.get('data'))
#         new_obj = http.request.env['some.model'].create({
#             'name': obj.get('name'),
            
#         })
#         print new_obj,'555555'
#     	# campuses= http.request.env['school.school'].sudo().search([])
#         # return http.request.render('school_ems.campus_list')

