# -*- coding: utf-8 -*-
# See LICENSE file for full copyright and licensing details.

import time
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError, Warning as UserError
from datetime import datetime


class SchoolWarning(models.Model):
	''' Defining a Teacher information '''
	_name = 'student.warning'
	_description = 'Warning Message'
	_inherit = ['mail.thread','ir.needaction_mixin']
	_order = "date desc"

	student_id = fields.Many2one('student.student','Student Name')
	name = fields.Text("Warning Message", required=True)
	state = fields.Selection([('draft', 'Draft'), ('approve', 'Warning Received By Student')],
							 'State', readonly=True, default='draft')
	date = fields.Date('Date', required=True,
					   help="Date of Warning",
					   default=lambda * a: time.strftime('%Y-%m-%d'))
	roll_no = fields.Char(string="Roll Number")
	standard_id = fields.Char( string="Class")
	


	@api.onchange('student_id')
	def onchange_student(self):
		'''Method to get standard and roll no of student selected'''
		if self.student_id:
			
			self.roll_no = self.student_id.roll_no
			self.classes=self.student_id.standard_id
			self.student_code=self.student_id.student_code
			


	@api.onchange('student_code')
	def onchange_student33(self):
		'''Method to get standard and roll no of student selected'''
		rec=self.env['student.student'].search([])
		for x in rec:
			if self.student_code==x.student_code :
				self.campus=x.school_id.id
				self.program=x.program_id.id
				self.course_level=x.semester_id.id
				self.shift=x.medium_id.id
				self.classes=x.standard_id
				self.student_id=x.id
				self.roll_no = x.roll_no
			if self.student_code==False:
				self.campus=False
				self.program=False
				self.course_level=False
				self.shift=False
				self.classes=False
				self.student_id=False
				self.roll_no = False




				
				

	@api.multi
	def warning_confirm(self):
		'''Method to change state to done'''


		rec=self.env['student.warning'].search([])
		obj=self.env['student.student'].search([])
		count=0
		for x in rec:
			if x.student_code==self.student_code:
				count=count+1

		if count==1:
			self.write({'warning_type':'1st Warning'})
			student = self.env.ref('school.warning_message_send_to_students')
			self.env['mail.template'].browse(student.id).send_mail(self.id, force_send=True)
			self.write({'state': 'approve'})

		if count==2:
			self.write({'warning_type':'2nd Warning'})
			student = self.env.ref('school.warning_message_send_to_students')
			self.env['mail.template'].browse(student.id).send_mail(self.id, force_send=True)
			self.write({'state': 'approve'})
		if count==3:
			self.write({'warning_type':'3rd Warning'})
			student = self.env.ref('school.terminate_message_send_to_students')
			self.env['mail.template'].browse(student.id).send_mail(self.id, force_send=True)
			self.write({'state': 'approve'})
			for y in obj:
				if self.student_code==y.student_code:
					y.state='block'




				
				






	# @api.multi
	# def unlink(self):
	# 	for rec in self:
	# 		if rec.state !='draft':
	# 			raise ValidationError(_('''You can delete the entry only in draft state !'''))
	# 	return super(SchoolWarning, self).unlink()

