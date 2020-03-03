# -*- coding: utf-8 -*-
# See LICENSE file for full copyright and licensing details.

import time
# import re
from datetime import date, datetime
from odoo import models, fields, api
from odoo.tools.translate import _
from odoo.modules import get_module_resource
# from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT
from odoo.exceptions import except_orm
from odoo.osv import expression
from odoo.exceptions import ValidationError,UserError
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT



class StudentStudent(models.Model):
	''' Defining a student information '''
	_inherit = 'student.student'
	

	ticket_test = fields.Many2one('website.support.ticket',string="Enq. Number", domain="[('status', '=', 'add-application')]")
	
	# @api.onchange('ticket_test')
	# def remoove_online_enquiry(self):
	# 	res=self.ticket_test.ticket_no
	# 	if res:
	# 		self.state=='done'
	# 		print 'eeeeeeeeeeeeeeeeee'
	# 	else:
	# 		print 'rrrrrrrrrrrrrrrrr'


		



	@api.onchange('ticket_test')
	def _ticket_number(self):
		if self.ticket_test:
			# raise UserError(str(self.same_address))
			self.name = self.ticket_test.name
			self.last = self.ticket_test.last_name
			self.email = self.ticket_test.email
			self.mobile = self.ticket_test.mobile
			self.school_id = self.ticket_test.campus_name.com_name

	@api.one
	def _check_status(self):
		f=self.env['website.support.ticket'].search([])
		if f.status == "followup":
			return True
	# @api.depends
	# def _adding_names(self):
	# 	self.fullname=self.name+self.last

			
			
	# @api.model
	# def create(self, vals):
	# 	res = super(StudentStudent, self).create(vals)
	# 	if res.ticket_test:
	# 		res.ticket_number.button_admit()
	# 	return res

