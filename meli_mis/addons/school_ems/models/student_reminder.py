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



	@api.onchange('student_id')
	def get_student_email(self):
		self.email=self.student_id.email



	
					# employee = self.env.ref('school_ems.student_reminder_message')
					# self.env['mail.template'].browse(employee.id).send_mail(self.id, force_send=True)
				# return response.text
		
		
	# @api.onchange('due_date')
	# def get_student_due_date(self):
		
		

		# today = self.date 
		# date_1 = datetime.datetime.strptime(today,'%Y-%m-%d')
		# end_date = date_1 + datetime.timedelta(days=4)
		# self.due_date=end_date
		
		# tomorrow = today + datetime.timedelta(4)
		# dd=datetime.datetime.strftime(tomorrow,'%Y-%m-%d')
		# print dd,"00000000000000000000000000000000000000"

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


			
			

	




		


		
			
				
					

				
				




			








	
		