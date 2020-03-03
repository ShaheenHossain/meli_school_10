# -*- coding: utf-8 -*-
##############################################################################
#
#    This module uses OpenERP, Open Source Management Solution Framework.
#    Copyright (C) 2017-Today Sitaram
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>
#
##############################################################################


from odoo.addons.web.controllers.main import Home
from odoo import http
from odoo.http import request


class WebsiteDesign(Home):

    @http.route(auth='public')
    def index(self, data={}, **kw):
        response = super(WebsiteDesign, self).index(**kw)
        if request.env.user.user_type:
            if request.env.user.user_type == "student":
                topics = request.env['tomorrows.topic'].get_topics()
                data['tomorrows_topic'] = topics
            return http.request.render('website_design.student_dashboard', data)
        else:
            return response

    @http.route('/student/leaveRequest', type='http', auth="public", website=True)
    def render_leave_request_form(self, **kw):
        if request.env.user.user_type and request.env.user.user_type == "student":
            return request.render('website_design.leaveRequest', {})
        return request.render('website.404', {})

    @http.route('/student/feedBackFrom', type='http', auth="public", website=True)
    def render_feedback_form(self, **kw):
        if request.env.user.user_type and request.env.user.user_type == "student":
            return request.render('website_design.feedBackFrom', {})
        return request.render('website.404', {})

    @http.route('/student/transferRequest', type='http', auth="public", website=True)
    def render_transfer_request_form(self, **kw):
        if request.env.user.user_type and request.env.user.user_type == "student":
            return request.render('website_design.transferRequest', {})
        return request.render('website.404', {})

    @http.route('/tearcher/tomorrowsTopic', type='http', auth="public", website=True)
    def render_tomorrows_topic_form(self, **kw):
        if request.env.user.user_type and request.env.user.user_type == "teacher":
            teacher = request.env['school.teacher'].search([]).filtered(lambda x: x.name.lower() == request.env.user.name.lower())
            if teacher and len(teacher) == 1:
                classes = teacher.standard_id.read(['display_name'])
            return request.render('website_design.tomorrowsTopic', {'classes': classes or []})
        return request.render('website.404', {})

    @http.route('/teacher/saveTomorrowsTopic', type='http', auth="public", website=True)
    def render_save_tomorrows_topic_form(self, **kw):
        if request.env.user.user_type and request.env.user.user_type == "teacher":
            tomorrows_topic = request.env['tomorrows.topic'].create({
                'name': kw.get('topic', False),
                'topic_date': kw.get('topic_date', False),
                'class_id': kw.get('classSelection', False)
            })
            return request.redirect('/tearcher/tomorrowsTopic')
            # return request.render('website_design.tomorrowsTopic', {'result': "success" if tomorrows_topic else "fail"})
