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

import datetime

from odoo import models, fields, api, _


class TomorrowsTopic(models.Model):
    _name = "tomorrows.topic"

    name = fields.Char("Topic Name")
    topic_date = fields.Date("Date")
    class_id = fields.Many2one('school.standard', string="Class")

    @api.model
    def get_topics(self):
        user = self.env.user
        vals = []
        if user.user_type == "student":
            student = self.env['student.student'].search([('name', '=', user.name)])
            if student:
                today = datetime.date.today() + datetime.timedelta(days=1)
                topics = self.search([('topic_date', '=', today.strftime("%Y-%m-%d")), ('class_id', '=', student.standard_id.id)])
                for topic in topics:
                    vals.append({
                        'teacher': topic.create_uid.name,
                        'topic_date': topic.topic_date,
                        'content': topic.name,
                        'class': student.standard_id.display_name
                    })
        return vals

