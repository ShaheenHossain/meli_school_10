import requests
import time
from datetime import date

from datetime import datetime
from odoo.exceptions import ValidationError,UserError


from odoo.tools import DEFAULT_SERVER_DATE_FORMAT


from odoo import models,api,fields,_


class student_fee_inherited(models.Model):
	_inherit="student.payslip"




	email=fields.Char(string="Email")
	due_date=fields.Date(string="Due Date")
	barcode=fields.Char(string="Barcode")



	@api.onchange('student_id')
	def get_student_email(self):
		self.email=self.student_id.email



	

class student_transfer_inherited(models.Model):
	_inherit = 'student.transfer'


	no_of_days=fields.Char(string="Previous Class Days")



	# @api.onchange('student_name')
	# def student_transfer_class_days(self):
	# 	res=self.env['student.student'].search([('name','=',self.student_name.name)])
	# 	rec=res.standard_id.start_date
	# 	rec1=date.today()
	# 	print rec,"--------------",rec1,"==================="
	# 	start_date = datetime.strptime(str(rec), "%Y-%m-%d")
	# 	end_date = datetime.strptime(str(rec1), "%Y-%m-%d")
	# 	# date = datetime.strptime(str(rec), DEFAULT_SERVER_DATE_FORMAT)
	# 	# enddate = datetime.strptime(str(rec1),DEFAULT_SERVER_DATE_FORMAT)
	# 	days = (end_date - start_date).days 

		
	# 	print(days)
	#('semester_id','=',self.semester_id.name),('medium_id','=',self.medium_id.name),('state','=','running')


class student_assign_class(models.Model):
	_inherit='student.student'


	due_date=fields.Date(string="Due Date")
	promotion_status=fields.Char(string="Promotion Status")



	@api.multi
	def assining_class(self):
		run_class_list = []
		class_names = self.env['school.standard']
		names = class_names.search([('school_id','=',self.school_id.id),
									('standard_id','=',self.program_id.id),
									('semester_id','=',self.semester_id.id),
									('medium_id','=',self.medium_id.id),
									('state','=','running')
									])
		for classes in names:
			run_class_list.append({'name': str(classes.standard),
									'campus':str(classes.school_id.name),
									'program_id':str(classes.standard_id.name),
									'level':str(classes.semester_id.name),
									'remaining_seats':str(classes.remaining_seats),
									'start_date':str(classes.start_date),
									'end_date':str(classes.end_date),
									})
		return {
			'type': 'ir.actions.act_window',
			'res_model': 'class.assign',
			'view_id': self.env.ref('school_ems.class_assign_wizard_view').id,
			'view_type': 'form',
			'view_mode': 'form',
			'data': None,
			'target': 'new',
			'context':{
				'default_class_assign':run_class_list
				}
			}
	@api.multi
	def assining_class1(self):
		run_class_list = []
		class_names = self.env['school.standard']
		names = class_names.search([('school_id','=',self.school_id.id),
									('standard_id','=',self.program_id.id),
									('semester_id','=',self.semester_id.id),
									('medium_id','=',self.medium_id.id),
									('add_final_date','!=',datetime.today().date()),
									('state','in',('running','draft')),
									])
		for classes in names:
			run_class_list.append({'name': str(classes.standard),
									'campus':str(classes.school_id.name),
									'program_id':str(classes.standard_id.name),
									'level':str(classes.semester_id.name),
									'remaining_seats':str(classes.remaining_seats),
									'start_date':str(classes.start_date),
									'end_date':str(classes.end_date),
									'state':str(classes.state)
									})
		return {
			'type': 'ir.actions.act_window',
			'res_model': 'class.assign',
			'view_id': self.env.ref('school_ems.class_assign_wizard_view').id,
			'view_type': 'form',
			'view_mode': 'form',
			'data': None,
			'target': 'new',
			'context':{
				'default_class_assign':run_class_list
				}
			}
		

	
	@api.onchange('standard_id')
	def get_values(self):
		

		rec=self.env['school.standard'].search([('standard','=',self.standard_id.standard)])
		count = 0
		for obj in rec.student_ids:
			count += 1
		self.roll_no = count


	@api.constrains('nid')
	def VeryfyingTazkiraNnumber(self):
		rec=self.env['student.student'].search([])
		for x in rec:
			if self.nid==x.nid:
				if x.id=='terminate':
					raise UserError(_('This Student in BlackList'))



class AssigingClasses(models.Model):
	_name = "class.assign"

	class_assign = fields.One2many('class.assign.lines', 'm2o', string="Runing Classes")

	
	@api.constrains('class_assign')
	def classes_selection_validation(self):
		count = 0
		for obj in self.class_assign:
			if obj.assign_class == True:
				count = count+1
		if count != 1:
			raise UserError("Please select any one Class")

	@api.multi
	def student_class_assigning(self):
		obj = self.env['school.standard'].search([])
		active_id = self.env.context.get('active_id')
		students = self.env['student.student'].search([('id','=',active_id)])
		for rec in self.class_assign:
			if rec.assign_class == True:
				for obj1 in obj:
					if rec.name == obj1.standard:
						students.standard_id = obj1.id
						students.roll_no=len(obj1.student_ids)
						students.division = obj1.division_id.name
						students.start_class=str(obj1.start_date)+ '  to  ' + str(obj1.end_date)
						students.state='done'
						

class AssigingClassesLines(models.TransientModel):
	_name = "class.assign.lines"

	name = fields.Char("Class", readonly="1")
	campus = fields.Char("Campus", readonly="1")
	program_id = fields.Char("Program", readonly="1")
	level = fields.Char("Level", readonly="1")
	remaining_seats = fields.Char('Available', readonly="1")
	start_date = fields.Char('State Date', readonly="1")
	end_date = fields.Char('End Date', readonly="1")
	assign_class = fields.Boolean(string="Assign")
	state=fields.Char(string="State")
	m2o = fields.Many2one('class.assign',"M2O")


class StudentAnnouncement(models.Model):
	_name = 'announcement.announcement'
	_rec_name="announcement_type"
	_inherit = ['mail.thread','ir.needaction_mixin']

	announcement_type=fields.Selection([('class_based','Class Based Announcements'),('shift_based','Shift Based Announcements'),('campus_based','Campus Based Announcements')],string='Announcement Type')
	campus=fields.Many2one('school.school',string="Campus")
	program=fields.Many2one('standard.standard',string="Program")
	level_id=fields.Many2one('standard.semester',string="Course Level")
	class_id=fields.Many2one('school.standard',string="Class",ondelete='cascade', index=True, copy=False)
	shift_id=fields.Many2one('standard.medium',string="Shift")
	note=fields.Text('Message')
	state=fields.Selection([('draft','Draft'),('send','Sent')], default='draft')
	email=fields.Char('Email')
	student_name=fields.Char(string='Student')




	@api.multi
	def warning_sent_to_students(self):
		rec=self.env['student.student'].search([])
		if self.announcement_type=='class_based':
			for x in rec:
				if self.campus.name==x.school_id.name and self.program.name==x.program_id.name and self.level_id.name==x.semester_id.name and self.shift_id.code==x.medium_id.code and self.class_id.standard==x.standard_id.standard:
					if x.state=='done':
						self.email=x.email
						self.student_name=x.name
						student = self.env.ref('school_ems.students_announcements')
						self.env['mail.template'].browse(student.id).send_mail(self.id, force_send=True)
					self.write({'state':'send'})

		if self.announcement_type=='shift_based':
			for x in rec:
				if self.campus.name==x.school_id.name and self.program.name==x.program_id.name and self.level_id.name==x.semester_id.name and self.shift_id.code==x.medium_id.code :
					if x.state=='done':
						self.email=x.email
						self.student_name=x.name
						student = self.env.ref('school_ems.students_announcements')
						self.env['mail.template'].browse(student.id).send_mail(self.id, force_send=True)
					self.write({'state':'send'})

		if self.announcement_type=='campus_based':
			for x in rec:
				if self.campus.name==x.school_id.name:
					if x.state=='done':
						self.email=x.email
						self.student_name=x.name
						student = self.env.ref('school_ems.students_announcements')
						self.env['mail.template'].browse(student.id).send_mail(self.id, force_send=True)
					self.write({'state':'send'})


					


			
			

	




		


		
			
				
					

				
				




			








	
		