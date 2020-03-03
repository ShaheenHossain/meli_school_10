import time
import re
import requests
import math

import datetime
from datetime import datetime, timedelta, date
import pandas as pd
from dateutil import relativedelta
import dateutil.parser
from openerp.exceptions import UserError
from twilio.rest import Client



from odoo import models, fields, api,_




class teacher_inherited(models.Model):
	_inherit='school.teacher'

	counting=fields.Char(string="Count",compute="_get_default_name")
	extra_class=fields.Char(string="Extra Class",compute="_get_default_name")
	history=fields.Char(string="Class History",compute="_get_default_name")
	update_subjects=fields.Char(string="Teacher Subjects",compute="_get_default_name")
	

	@api.multi 
	def _get_default_name(self):
		data_obj = self.env['student.regular.timetable'].search([('teacher','=',self.employee_id.name),('status','=','running')])
		self.update_subjects = len(data_obj)
		self.counting=len(data_obj)
		rec = self.env['student.regular.timetable'].search([('substistute','=',self.employee_id.name),('status','=','running')])
		self.extra_class=len(rec)
		obj=self.env['student.regular.timetable'].search([('teacher','=',self.employee_id.name),('status','=','close')])
		self.history=len(obj)


	@api.multi
	def teacher_class_timetable1(self):
		return{
        	'type': 'ir.actions.act_window',
        	'name':'Extra Timetable',
        	'view_mode': 'tree',
        	'view_id': self.env.ref('school_ems.student_substistute_process').id,
        	'res_model': 'substistute.teacher',
        	'domain':[('s_teacher','=',self.employee_id.name)],
    		}

	@api.multi
	def teacher_class_timetable(self):
		return{
        	'type': 'ir.actions.act_window',
        	'name':'Timetable',
        	'view_mode': 'tree',
        	'view_id': self.env.ref('school_ems.tyd_student_timetable_view').id,
        	'res_model': 'tyd.teacher.timetable',
        	'domain':[('teacher.id','=',self.id),('classes.state','=','running')],
        	'context':{'group_by':['course_level','classes','name']}
    		}

	@api.multi
	def teacher_class_timetable2(self):
		return{
    		'type': 'ir.actions.act_window',
        	'name':'Extra Timetable',
        	'view_mode': 'tree',
        	'res_model': 'student.regular.timetable',
        	'domain':[('teacher','=',self.employee_id.name),('status','=','close')],

    		}



class warning_message_for_students(models.Model):
	_inherit = 'student.warning'


	campus=fields.Many2one('school.school',string='Campus')
	program=fields.Many2one('standard.standard',string='Program')
	course_level=fields.Many2one('standard.semester',string="Course Level")
	student=fields.Many2one('student.student',string='Student Name')
	shift=fields.Many2one('standard.medium',string="Shift")
	classes=fields.Many2one('school.standard',string="Class")
	student_code=fields.Char(string="Student Code")
	warning_type=fields.Char('Type Of Warning',readonly=True)


	# @api.constrains('student_code')
	# def show_exception(self):
	# 	rec=self.env['student.warning'].search([])
	# 	for x in rec: 
	# 		if x.student_code==self.student_code:
	# 			raise UserError(_('Already Given Warning for this Student'))


class subjects_inherited(models.Model):
	_inherit="subject.subject"


	program=fields.Many2one('standard.standard',string="Program")
	course_level=fields.Many2one('standard.semester',string="Course Level")

class student_subjects(models.Model):
	_name = 'student.subjects'


	name=fields.Char(string="Subject Name")
	program_id=fields.Many2one('standard.standard',string='Program')
	semester_id=fields.Many2one('standard.semester',strint='Course Level')
	campus_id=fields.Many2one('school.school',string='Campus')
	sub_code=fields.Char(string='Subject Code')

class classes_inherited(models.Model):
	_inherit='school.standard'

	@api.model
	def _needaction_domain_get(self):
		return[('state','=','finish')]

	@api.multi
	def cron_start_stop(self):
		running_class_ids = self.search([('start_date', '=', fields.Date.today())])
		running_class_ids.update({
		'state':'running'
		})
		close_class_ids = self.search([('end_date', '=', fields.Date.today())])
		close_class_ids.update({'state':'close'})
		rec=self.env['school.standard'].search([])
		for x in rec:
			date=x.end_date
			datetime_object = datetime.strptime(date, '%Y-%m-%d').date()
			yesterday =datetime_object - timedelta(days=2)
			if datetime.now().date() == yesterday:
				x.state='finish'
		return

	@api.constrains('division_id')
	def onchange_class_room(self):
		data=self.env['school.standard'].search([])
		for rec in data:
			if rec.state == 'running':
				if rec.end_date!=False and self.division_id.name==rec.division_id.name and self.school_id.name == rec.school_id.name:
					d=datetime.date(datetime.now())
					d2=datetime.strptime(rec.end_date, '%Y-%m-%d')
					d3=datetime.strptime(str(d), '%Y-%m-%d')
					delta=d2-d3
					raise UserError(_('In This Class Room Already Class Is GOing On."%s" days Left')%(delta.days))


	@api.multi
	def sending_to_students(self):
		rec=self.env['standard.standard'].search([('name','=',self.standard_id.name)])
		rec1=self.env['student.subjects'].search([('program_id','=',self.standard_id.name),('semester_id','=',self.semester_id.name)])
		rec2=self.env['final.results'].search([])
		var = self.env['student.student'].search([])
		length=len(rec1)
		for students in  self.student_ids:
			count = 0
			fail_count=0
			if self.code=='DEL':
				for i in rec2:
					for j in i.talk_ids:
						if  i.class_id.standard == self.standard and j.name.student_code==students.student_code:
							if j.result=='Pass':
								count+=1
							if j.result=='Fail':
								fail_count+=1 
				if count==length:
					if self.standard:
						var_list = []
						for a in var:
							if a.student_code==students.student_code:

								if var:
									ele = {
										'program_id': self.standard_id.name,
										'level_id':self.semester_id.name,
										'roll_no':self.roll_no,
										'standard_id': self.standard,
										'start_date': self.start_date,
										'end_date':self.end_date,
										}
									var_list.append(ele)
							a.history_ids = var_list
							for x in rec.semester_ids:
								if x.sequence==self.semester_id.sequence+1 :
									a.semester_id=x.id
									a.standard_id=False
									a.division=False
									a.roll_no=False
									a.start_class=False
									a.promotion_status='Promoted To Next Level'
									a.state='draft'
									break

				if count!=length and fail_count>2:
					if self.standard:
						var_list = []
						for a in var:
							if a.student_code==students.student_code:
								if var:
									ele = {
										'program_id': self.standard_id.name,
										'level_id':self.semester_id.name,
										'standard_id': self.standard,
										'start_date': self.start_date,
										'end_date':self.end_date,
										'roll_no':self.roll_no

										
										}
									var_list.append(ele)
							
							a.history_ids = var_list
							for x in rec.semester_ids:
								if x.sequence==self.semester_id.sequence+1 :
									
									a.standard_id=False
									a.division=False
									a.roll_no=False
									a.start_class=False
									a.promotion_status='repeat'
									a.state='draft'
									break
				


			if self.code=='TYD':
				for i in rec2:
					for j in i.subject_id:
						if  i.class_id.standard == self.standard and j.name.name==students.name:
							if (j.total)>50:
								count+=1
							if (j.total)<50:
								fail_count+=1 
	
			var = self.env['student.student'].search([])
			if count==length:
				if self.standard:
					var_list = []
					for a in var:
						if a.student_code==students.student_code:
							if var:
								ele = {
									'program_id': self.standard_id.name,
									'level_id':self.semester_id.name,
									'standard_id': self.standard,
									'start_date': self.start_date,
									'end_date':self.end_date,
									'roll_no':self.roll_no
									}
								var_list.append(ele)
						
						a.history_ids = var_list
						for x in rec.semester_ids:
							if x.sequence==self.semester_id.sequence+1 :
								a.semester_id=x.id
								a.standard_id=False
								a.division=False
								a.roll_no=False
								a.start_class=False
								a.promotion_status='Promoted To Next Level'
								a.state='draft'
								break

			if count!=length and fail_count>2:
				if self.standard:
					var_list = []
					for a in var:
						if a.student_code==students.student_code:
							if var:
								ele = {
									'program_id': self.standard_id.name,
									'level_id':self.semester_id.name,
									'standard_id': self.standard,
									'start_date': self.start_date,
									'end_date':self.end_date,
									
									}
								var_list.append(ele)
						
							a.history_ids = var_list

							for x in rec.semester_ids:
								if x.sequence==self.semester_id.sequence+1 :
									a.standard_id=False
									a.division=False
									a.roll_no=False
									a.start_class=False
									a.promotion_status='repeat'
									a.state='draft'
									break
			

	@api.one
	@api.model
	def _compute_ending_date(self):
		rec=self.env['standard.standard'].search([])
		for x in rec:
			for y in x.semester_ids:
				if self.start_date:
					if self.standard_id.name==x.name and self.semester_id.name==y.name:
						print self.start_date,'2222222222222222'
						enddate = pd.to_datetime(self.start_date) + pd.DateOffset(days=y.course_duration)
						self.end_date=enddate



class student_results_inherited(models.Model):
	_inherit='student.student'

	def MuslimInvitation(self):
		print "rrrrrrrrrrrrrrrrrrrrrrrrrrr"
		rec=self.env['student.student'].search([])
		for x in rec:
			if str(datetime.now().date()) == str(x.admission_date):
				print x.email,"33333333333333333"
				student = self.env.ref('school_ems.fsgfsgfjhsgfadssadeefdsfsd')
				self.env['mail.template'].browse(student.id).send_mail(self.id, force_send=True)
				

	
	@api.multi
	def student_results(self):
		if self.program_id.code=='DEL':
			print "55555555555555"
			return{
		        'type': 'ir.actions.act_window',
		        'name':'Result',
		        'view_mode': 'tree',
		        'res_model': 'oyd.exam',
		        'view_id': self.env.ref('school_ems.student_oyd_results').id,
		        'domain':[('name.pid','=',self.pid)],
		        'context': {
			        'create':False,
			        'edit' : False,
			        'delete' : False,
			        'group_by':'level_id'

			        
			        }
		    	}
		if self.program_id.code=='TYD':
			return{
		        'type': 'ir.actions.act_window',
		        'name':'Result',
		        'view_mode': 'tree',
		        'res_model': 'student.finalexam',
		        'view_id': self.env.ref('school_ems.student_midexam_results777').id,
		        'domain':[('name.pid','=',self.pid),('sub123.state','=','confirm')],
		        'context': {
			        'create':False,
			        'edit' : False,
			        'delete' : False,
			        'group_by':'level_id'
			        
			        }
		    	}
		if self.program_id.code=='TT':
			return{
		        'type': 'ir.actions.act_window',
		        'name':'Result',
		        'view_mode': 'tree',
		        'res_model': 'talk.talk',
		        'view_id': self.env.ref('school_ems.student_midexam_results7777').id,
		        'domain':[('name.pid','=',self.pid)],
		        'context': {
			        'create':False,
			        'edit' : False,
			        'delete' : False,
			        'group_by':'semester_subjects'
			        
			        }
		    	}


	@api.multi
	def send_student_fee_reminder1(self):
		print "3333333333333"
		b=str(datetime.today())
		d = dateutil.parser.parse(b).date()
		rec=self.env['student.student'].search([])
		for x in rec:
			if  str(d)==str(x.date_of_birth) :
				sid='AC1f14a7f931620ce90d26e007d8f93783'
				token='a74b10489ae826dee260b9f52d63e513'
				client = Client(sid,token)
				from_whatsapp_number='whatsapp:+14155238886'
				to_whatsapp_number='whatsapp:+91'+str(x.mobile)
				client.messages.create(body='Dear '+x.name+' many more happy returns Of the day',
                       from_=from_whatsapp_number,
                       to=to_whatsapp_number)

				student = self.env.ref('school_ems.students_happy_birthday_wishes')
				self.env['mail.template'].browse(student.id).send_mail(x.id, force_send=True)

			# if  str(d)==str(x.due_date) :
			# 	url = "https://www.fast2sms.com/dev/bulk"
			# 	payload = "sender_id=FSTSMS&message=Dear"+str(x.name)+" You need to pay  Due Amount. &language=english&route=p&numbers="+str(x.mobile)
			# 	headers = {
			# 	'authorization': "WnE3TqV6AIv5qf8ir5PKnVjXxCzhCFCHasABU58gXRhO9JFqFluWZXvlbsv9",
			# 	'Content-Type': "application/x-www-form-urlencoded",
			# 	'Cache-Control': "no-cache",
			# 		}
			# 	response = requests.request("POST", url, data=payload, headers=headers)

	@api.multi
	def student_regular_timetable(self):
		return{
		        'type': 'ir.actions.act_window',
		        'name':'Student Class Time Table',
		        'view_mode': 'tree',
		        'view_id': self.env.ref('school_ems.tyd_student_timetable_view11').id,
		        'res_model': 'tyd.teacher.timetable',
		        'domain':[('classes.standard','=',self.standard_id.standard)],
		        'context': {
			        'create':False,
			        'edit' : False,
			        'delete' : False,
			       
			        }
		    	}
	@api.multi
	def student_exam_timetable(self):
		return{
		        'type': 'ir.actions.act_window',
		        'name':'Student Exam Time Table',
		        'view_mode': 'tree',
		        'view_id': self.env.ref('school_ems.student_exam_timetable_treeview11').id,
		        'res_model': 'student.exam.schdule',
		        'domain':[('class_id','=',self.standard_id.standard)],
		        'context': {
		        	'group_by':['course_level'],
			        'create':False,
			        'edit' : False,
			        'delete' : False,

			       
			        }
		    	}

	@api.multi
	def student_makeup_exam_timetable(self):
		if self.program_id.code == 'DEL':
			return{
			        'type': 'ir.actions.act_window',
			        'name':'MakeUp Exam Time Table',
			        'view_mode': 'tree',
			        'view_id': self.env.ref('school_ems.tyd_makeup_scheduling_tree').id,
			        'res_model': 'tyd.schdule',
			        'domain':[('s_name.student_code','=',self.student_code)],
			        'context': {
			        	
				        'create':False,
				        'edit' : False,
				        'delete' : False,

				       
				        }
			    	}

		if self.program_id.code == 'TYD':
			return{
			        'type': 'ir.actions.act_window',
			        'name':'MakeUp Exam Time Table',
			        'view_mode': 'tree',
			        'view_id': self.env.ref('school_ems.tyd_makeup_scheduling_tree').id,
			        'res_model': 'tyd.schdule',
			        'domain':[('s_name.student_code','=',self.student_code)],
			        'context': {
			        	
				        'create':False,
				        'edit' : False,
				        'delete' : False,

				       
				        }
			    	}
			
		if self.program_id.code == 'TT':
			return{
			        'type': 'ir.actions.act_window',
			        'name':'MakeUp Exam Time Table',
			        'view_mode': 'tree',
			        'view_id': self.env.ref('school_ems.student_makeup_scheduling_tree').id,
			        'res_model': 'schdule.makeup',
			        'domain':[('s_name.student_code','=',self.student_code)],
			        'context': {
				        'create':False,
				        'edit' : False,
				        'delete' : False,
				        }
			    	}


class payment_inherited(models.Model):
	_inherit= "account.payment"


	due_date=fields.Date(string="Due Date")
	note=fields.Char(string="Note")
# class AccountInvoiceLine(models.Model):
# 	_inherit = 'account.invoice.line'

# 	disc=fields.Float(string='Disc.(%)')



	



    	




	