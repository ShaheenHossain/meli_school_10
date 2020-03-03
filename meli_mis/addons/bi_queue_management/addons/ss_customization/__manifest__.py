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

{
    'name': "School ERP Customization",
    'version': "10.0.0.0",
    'summary': "School ERP Customization",
    'category': 'Customization',
    'description': """
        School ERP Customization 
    """,
    'author': "Sitaram Solutions",
    'website': "sitaramsolutions.com",
    'depends': ['base','school','purchase'],
    'data': [
        'report/report.xml',
        'report/timetable.xml',
        'report/daily_class_reporting.xml',
        'data/class_start_stop_cron.xml',
        'data/mail_template_data.xml',
        'views/menu_items.xml',
        'views/inherited_class.xml',      
        'views/inherited_teacher.xml'
        
    ],
    'demo': [],
    "license": "AGPL-3",
    'installable': True,
    'auto_install': False,
}
