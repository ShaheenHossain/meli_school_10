
import time
import requests
from lxml import etree
import json
from datetime import datetime
import datetime  
from datetime import date 
import calendar 
from dateutil.relativedelta import relativedelta as rd

from odoo import models, fields, api, _
from odoo.exceptions import Warning as UserError
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT
from odoo.exceptions import ValidationError

class TydDailyAttendance(models.TransientModel):
	_name = "tyd.daily.attendance"
	
	campus_id = fields.Many2one('school.school',"Campus")
	program_id = fields.Many2one('standard.standard','Program')
	semester_id = fields.Many2one("standard.semester","Semester")
	shift_id = fields.Many2one("standard.medium","Shift")
	division_id = fields.Many2one("standard.division","Room Number")
	date = fields.Date("Date", required=True)
	name = fields.Many2one("school.standard","Class", required=True)
	subjects = fields.Many2one("student.subjects","Subject", compute="period_onchange_action")
	periods = fields.Selection([('period_1','1st Period'),
								('period_2','2nd Period'),
								('period_3','3rd Period'),
								('period_4','4th Period'),
								('period_5','5th Period'),
								('period_6','6th Period'),
								('period_7','7th Period')], string="Periods")
	tt = fields.Char(string="Code")

	@api.onchange('program_id')
	def program_onchange_action(self):
		self.tt = self.program_id.code
		if self.tt == "TT":
			self.subjects = False
			self.periods = False



	@api.constrains('date')
	def validate_date_of_attendance(self):
		# obj_date=datetime.strptime(self.date, '%Y-%m-%d').date()
		current_date=fields.Datetime.now()

		if self.date <= self.name.start_date:
			raise UserError('Please Select date in between class dates')
		if self.date>current_date:
			raise UserError('Please Select Date after class is started')
		if self.date >= self.name.end_date:
			raise UserError('Please Select date in between class dates')


		




	# @api.onchange('periods')
	# def period_test(self):
	# 	days = dict(self._fields['periods'].selection).get(self.periods)
	# 	print days,"@@@@@@@@@@@@@@@@@@@@@@"
	# 	if days == "1st Period":
	# 		print "111222222222222222222222"

	@api.depends('periods')
	def period_onchange_action(self):
		date = str(self.date)
		if self.date != False:
			year, month, day  = (int(i) for i in date.split('-'))
			born = datetime.date(year, month, day)
			day = born.strftime("%A")

			tables = self.env['tyd.timetable'].search([])
			for time_table in tables:
				if self.name == time_table.classes:
					for days in time_table.saturday_id:
						day1 = dict(days._fields['name'].selection).get(days.name)
						if day1 == day:
							for period in days.period3:
								periods=dict(self._fields['periods'].selection).get(self.periods)
								if period.period == periods:
									self.subjects = period.subject.id




	@api.onchange('name')
	def name_onchange_action(self):
		self.division_id = self.name.division_id

	@api.multi
	def get_attendance_data(self):

		attendance = self.env['tyd.attendance'].search([])
		print len(attendance),"111111111111111111111111"

		self.division_id = self.name.division_id.id
		stud_obj = self.env['student.student']
		student_list = []
		for rec in self:
			if rec.name:
				stud_ids = stud_obj.search([('standard_id', '=',
											 rec.name.id),
											('state', '=', 'done')])
				for stud in stud_ids:
					# raise UserError(stud.photo)
					presents = 0
					absents = 0
					total = 0
					student_leave = self.env['studentleave.request'].search([('state', '=','approve'),
						('student_id', '=',stud.id),('standard_id', '=',rec.name.id),
						('course_level','=',rec.name.semester_id.name),('start_date', '<=',rec.date),('end_date', '>=',rec.date)])
					for attend in attendance:
						if attend.name == self.name and attend.state == 'done':
							for students in attend.attendance_lines:
								if stud.id == students.name.id:
									total = total + 1
									if students.is_present == True:
										presents = presents + 1
									if students.is_absent == True:
										absents = absents + 1
									
					if student_leave:
						student_list.append({'s_no': stud.roll_no,
											 'name': stud.id,
											 'photo':stud.photo,
											 'leave':"Approved",
											 'total_presents':presents,
											 'total_absents':absents,
											 'total_work_days':total,
											 'is_present':True,
											 'is_absent':True,
											 })

					else:
						student_list.append({'s_no': stud.roll_no,
											 'name': stud.id,
											 'photo':stud.photo,
											 'total_presents':presents,
											 'total_absents':absents,
											 'total_work_days':total,
											 'is_present':True,
											 'is_absent':False,
											 })

		for attends in attendance:
			if attends.name == self.name and attends.periods == self.periods and attends.date == self.date:
				record = attends.id
				return{
					'type': 'ir.actions.act_window',
					'res_model': 'tyd.attendance',
					'view_id': self.env.ref('school_ems.tyd_attendance_form').id,
					'view_type': 'form',
					'res_id'    : record,
					'view_mode': 'form',
					'groups':'school.group_school_attendance_officer',
					'context': {
						        'create':False,
						        'edit' : False,
						        'delete' : False,
	        					}
				}
			
		
		print "333333333333333333"
		return {
				'type': 'ir.actions.act_window',
				'res_model': 'tyd.attendance',
				'view_id': self.env.ref('school_ems.tyd_attendance_form').id,
				'view_type': 'form',
				'view_mode': 'form',
				'data': None,
				'groups':'school.group_school_attendance_officer',
				# 'target': 'new',
				'context':{
					'create':False,
					'edit' : False,
					'delete' : False,
					'default_name':self[0].name.id,
					'default_campus_id':self[0].campus_id.id,
					'default_program_id':self[0].program_id.id,
					'default_semester_id':self[0].semester_id.id,
					'default_shift_id':self[0].shift_id.id,
					'default_division_id':self[0].division_id.id,
					'default_date':self[0].date,
					'default_subjects':self.subjects.id,
					'default_attendance_lines':student_list,
					'default_periods':self[0].periods,
					'default_tt':self[0].tt
					}
				}

	@api.multi
	def attendance_form(self):
		# records = self.env['tyd.daily.attendance'].search([])
		# last_record = 0
		# for record in records:
		# 	last_record = record.id
		# if last_record != 0:
		# 	return {
		#         'type': 'ir.actions.act_window',
		#         'res_model' : 'tyd.daily.attendance',
		#         'view_mode' : 'form',
		#         'res_id'    : last_record,
		#         'target'    : 'inline',
		#         'nodestroy': True,
		#         }
		# elif last_record == 0:
		return {
	        'type': 'ir.actions.act_window',
	        'res_model' : 'tyd.daily.attendance',
	        'view_mode' : 'form',
	        'target'    : 'inline',
	        }


class TydDailyAttendanceNew(models.Model):
	_name = "tyd.attendance"


	campus_id = fields.Many2one('school.school',"Campus")
	state = fields.Selection([('draft','Draft'),
							  ('done','Done')], string="State", default="draft")
	program_id = fields.Many2one('standard.standard','Program')
	semester_id = fields.Many2one("standard.semester","Semester")
	shift_id = fields.Many2one("standard.medium","Shift")
	division_id = fields.Many2one("standard.division","Room Number")
	date = fields.Date("Date")
	name = fields.Many2one("school.standard","Class")
	subjects = fields.Many2one("student.subjects","Subject")
	periods = fields.Selection([('period_1','1st Period'),
								('period_2','2nd Period'),
								('period_3','3rd Period'),
								('period_4','4th Period'),
								('period_5','5th Period'),
								('period_6','6th Period'),
								('period_7','7th Period')], string="Periods")
	tt = fields.Char(string="Code")

	attendance_lines = fields.One2many('tyd.daily.attendance.lines','m2o', string="Students")

	@api.multi
	def confirm_action(self):
		# for z in self.attendance_lines:
		# 	z.state='done'
		obj=self.env['student.student'].search([])
		for x in obj:
			if x.semester_id.name==self.semester_id.name:
				for y in self.attendance_lines:
					if x.student_code==y.name.student_code:
						x.total_presents=y.total_presents
						x.total_absent=y.total_absents
						x.atten_leaves=y.leave
						x.total_attendance=y.total_work_days
		self.write({'state':'done'})
		return{
				'type': 'ir.actions.act_window',
				'res_model': 'tyd.daily.attendance',
				'view_id': self.env.ref('school_ems.tyd_student_attendance_form').id,
				'view_type': 'form',
				'view_mode': 'form',
				
				}
		


class TydDailyAttendancelines(models.Model):
	_name = "tyd.daily.attendance.lines"


	s_no = fields.Char(string="S.No")
	name = fields.Many2one("student.student","Name")
	photo = fields.Binary(string='Photo')
	m2o = fields.Many2one("tyd.attendance", string="M2O")
	is_present = fields.Boolean('Present', help="Check if student is present", default=True)
	is_absent = fields.Boolean('Absent', help="Check if student is absent", default=True)
	total_presents = fields.Integer(string="Presents")
	total_absents = fields.Integer(string="Absents")
	total_work_days = fields.Integer(string="Total Period")
	student_parent = fields.Char(string="")
	leave = fields.Char(string="Leave")
	
	

	# testing = fields.Boolean(string="test", default="True")


	@api.multi
	def present(self):
		print "111111111111111111"
		self.is_present = False
		self.is_absent = True
		

	@api.multi
	def absent(self):

		self.is_present = True
		self.is_absent = False
		



	


class TydDailyAttendanceReport(models.TransientModel):
	_name = "tyd.daily.report"

	class_name = fields.Many2one('school.standard',"Academic Class")
	start_date = fields.Date('Start Date')
	end_date = fields.Date('End Date')
	program_id = fields.Many2one('standard.standard','Program')
	semester_id = fields.Many2one("standard.semester","Semester")
	subjects = fields.Many2one("student.subjects","Subject")
	tt = fields.Char(string="Code")

	@api.onchange('program_id')
	def program_onchange_action(self):
		self.tt = self.program_id.code
		if self.tt == "TT":
			self.subjects = False
			self.periods = False



	@api.onchange('class_name')
	def getting_class_dates(self):
		rec=self.env['school.standard'].search([('standard','=',self.class_name.standard)])
		for x in rec:
			self.start_date=x.start_date
			self.end_date=x.end_date

	@api.multi
	def tyd_classwise_students_report(self):
		self.ensure_one()
		active_ids = self.env.context.get('active_ids', [])
		datas={
		'ids':active_ids,
		'model': 'tyd.daily.report',
		'form': self.read()[0]
		}
		return self.env['report'].get_action(self,'school_ems.tyd_class_attendance_report',data=datas)

class TydAttendanceReportRenderhtml(models.AbstractModel):
	_name = 'report.school_ems.tyd_class_attendance_report'

	def get_students(self,class_id,date_from,date_to,subjects):
		student_name = self.env['school.standard'].search([('standard','=',str(class_id[1]))])
		
		total_student = {}
		count = 1
		obj = self.env['tyd.attendance'].search([])
		for students in student_name.student_ids:
			name = []
			presents = 0  
			absents = 0
			total = 0
			leaves = 0
			for rec in obj:
				if subjects == False:
					if rec.name.standard == str(class_id[1]):
						if rec.date >= date_from and rec.date <= date_to:
							print "0000000000000000000"
							total = total+ 1
							for students_attendance in rec.attendance_lines:
								if students.name == students_attendance.name.name:
									if students_attendance.leave != "Approved":
										if students_attendance.is_present == True:
											presents = presents + 1
										else:
											absents = absents + 1
									else:
										leaves = leaves + 1
				else:
					if rec.name.standard == str(class_id[1]) and str(subjects[1]) == rec.subjects.name:
						if rec.date >= date_from and rec.date <= date_to:
							total = total+ 1
							for students_attendance in rec.attendance_lines:
								if students.name == students_attendance.name.name:
									if students_attendance.leave != "Approved":
										if students_attendance.is_present == True:
											presents = presents + 1
										else:
											absents = absents + 1
									else:
										leaves = leaves + 1

			name.extend([str(students.student_code),str(students.name),str(students.parent_id),presents,absents,leaves,total])
			total_student[count]=name
			count = count + 1
		print total_student,'22222222222'
		return total_student






	def class_details(self,class_id,subjects):
		classes = self.env['school.standard'].search([])
		subject = False
		if subjects != False:
			subject = str(subjects[1])
		class_details = []
		for dts in classes:
			if dts.standard == str(class_id[1]):
				class_details.extend([str(dts.standard_id.name),str(dts.semester_id.name),str(dts.standard),str(dts.medium_id.name),str(dts.start_date),str(dts.end_date),subject])
		return class_details



	@api.model
	def render_html(self, docids, data=None):
		register_ids = self.env.context.get('active_ids', [])
		date_from = data['form'].get('start_date')
		date_to = data['form'].get('end_date')
		class_id = data['form'].get('class_name')
		subjects = data['form'].get('subjects')


		

		get_data = self.get_students(class_id,date_from,date_to,subjects)
		class_details = self.class_details(class_id,subjects)
		
		docargs = {
		'doc_model':'tyd.daily.report',
		'data': data,
		'docs': class_details,
		'students':get_data,
		}
		return self.env['report'].render('school_ems.tyd_class_attendance_report', docargs)


	