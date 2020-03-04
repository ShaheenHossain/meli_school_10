# -*- coding: utf-8 -*-

import datetime
from datetime import date,time
from odoo import models, fields, api


class MoneteringNEvaluationDepartment(models.Model):
	_name = "employee.moneter"

	survey_type=fields.Selection([('student','Student'),('employee','Employee')],string="Survey Type",default='employee')
	name=fields.Many2one('school.school',string="Campus")
	date=fields.Date(string="Date",default=fields.Date.context_today,readonly=True)
	m_line_id=fields.One2many('employee.satisfation','lines_id')
	student_line_id=fields.One2many('student.survey','student_lines')

	program=fields.Many2one('standard.standard',string="Program")
	level_id=fields.Many2one('standard.semester',string="Course Level")
	class_id=fields.Many2one('school.standard',string="Class",ondelete='cascade', index=True, copy=False)
	shift_id=fields.Many2one('standard.medium',string="Shift")

	@api.multi
	def employee_survey_confirmation(self):
		self.m_line_id=False
		self.student_line_id=False

		if self.survey_type=='employee' and self.name:
			rec=self.env['hr.employee'].search([])
			employees=[]
			for x in rec:
				if self.name.name==x.school_id.name:
					employees.append(({'name':x.id,'emp_id':x.code,'designation':x.job_id.name,'date':self.date,'state':'draft','date_of_joinning':x.date_of_join,'campus':x.school_id.id}))
			self.m_line_id=employees
			for rec in self.m_line_id:
				rec._get_course_data()

		

		if self.survey_type=='student':
			obj=self.env['student.student'].search([])
			students=[]
			for i in obj:
				if self.level_id.id==i.semester_id.id and self.name.id==i.school_id.id and self.class_id.standard==i.standard_id.standard:
					students.append(({'s_id':i.student_code,'name':i.id,'course_level':i.semester_id.name,'d_joining':i.admission_date,'state':'draft'}))
			
			self.student_line_id=students
			for rec in self.student_line_id:
				rec._get_course_data()
		

	


class EmployeeSatisfactionForm(models.Model):

	_name = 'employee.satisfation'

	name=fields.Many2one("hr.employee",string="Employee Name")
	emp_id=fields.Char('Employee ID No.')
	date_of_joinning=fields.Date(string="Date of Joining")
	designation=fields.Char(string="Designation")
	campus=fields.Many2one('school.school',string="Campus")

	language_id=fields.One2many('employee.language.lines','language_lines')
	manager_id=fields.One2many('employee.manager.lines','manager_lines')
	enablement_id=fields.One2many('employee.enablement.lines','enablement_lines')
	alignment_id=fields.One2many('employee.alignment.lines','alignment_lines')
	developement_id=fields.One2many('employee.developement.lines','developement_lines')
	lines_id=fields.Many2one('employee.moneter')
	date=fields.Date('Date')
	suggetions1=fields.Text('Description')

	state=fields.Selection([('draft','Draft'),('done','Done')])
	total=fields.Integer('Total Marks',compute='_compute_marks')
	percentage=fields.Integer('Percentage',compute='_compute_marks')

	def _get_course_data(self):
		rec=self.env['survey.questions'].search([])
		courses=[]
		terms=[]
		material=[]
		employee=[]
		environment=[]
		for x in rec:
			for y in x.survey_lines_id:
				question_type = dict(x._fields['employee_question'].selection).get(x.employee_question)
				if x.name=='employee':
					self.language_id=False
					self.manager_id = False
					self.enablement_id = False
					self.alignment_id = False
					self.developement_id = False
					if question_type == 'About Muslim English Language':
						courses.append(({'term':y.question}))
					self.language_id=courses
					if question_type == 'Manager':
						terms.append(({'manager':y.question}))
					self.manager_id=terms
					if question_type == 'Enablement':
						material.append(({'enablement':y.question}))
					self.enablement_id=material
					if question_type == 'Alignment':
						employee.append(({'alignment':y.question}))
					self.alignment_id=employee
					if question_type == 'Development':
						environment.append(({'developement':y.question}))
					self.developement_id=environment

	@api.model
	def _compute_marks(self):
		count=0
		for x in self.language_id:
			if x.strong_agree==True:
				count=count+4
			if x.agree==True:
				count=count+3
			if x.dis_agree==True:
				count=count+2
			if x.neutral==True:
				count=count+1
			if x.strongly_disagree==True:
				count=count+0
		for x in self.manager_id:
			if x.strong_agree==True:
				count=count+4
			if x.agree==True:
				count=count+3
			if x.dis_agree==True:
				count=count+2
			if x.neutral==True:
				count=count+1
			if x.strongly_disagree==True:
				count=count+0
		for x in self.enablement_id:
			if x.strong_agree==True:
				count=count+4
			if x.agree==True:
				count=count+3
			if x.dis_agree==True:
				count=count+2
			if x.neutral==True:
				count=count+1
			if x.strongly_disagree==True:
				count=count+0

		for x in self.alignment_id:
			if x.strong_agree==True:
				count=count+4
			if x.agree==True:
				count=count+3
			if x.dis_agree==True:
				count=count+2
			if x.neutral==True:
				count=count+1
			if x.strongly_disagree==True:
				count=count+0
		for x in self.developement_id:
			if x.strong_agree==True:
				count=count+4
			if x.agree==True:
				count=count+3
			if x.dis_agree==True:
				count=count+2
			if x.neutral==True:
				count=count+1
			if x.strongly_disagree==True:
				count=count+0
		self.total=count
		self.percentage=(count*100)/72



	
	@api.multi
	def employee_survey_submission(self):
		self.write({'state':'done'})

	

	


class AboutMuslimEnglishLanguage(models.Model):
	_name='employee.language.lines'

	term=fields.Char(string="Questions")
	strong_agree=fields.Boolean(string="Strongly Agree")
	agree=fields.Boolean(string="Agree")
	neutral=fields.Boolean(string="Neutral")
	dis_agree=fields.Boolean(string="Dis Agree")
	strongly_disagree =fields.Boolean(string="Strongly Disagree")
	reason=fields.Char('Reason for Disagree')
	language_lines=fields.Many2one('employee.satisfation')
	@api.onchange('strong_agree')
	def onchanging_strong_agree(self):
		if self.strong_agree!=0:
			self.agree=0
			self.neutral=0
			self.dis_agree=0
			self.strongly_disagree=0

	@api.onchange('agree')
	def onchanging_agree(self):
		if self.agree!=0:
			self.strong_agree=0
			self.neutral=0
			self.dis_agree=0
			self.strongly_disagree=0

	@api.onchange('neutral')
	def onchanging_neutral(self):
		if self.neutral!=0:
			self.strong_agree=0
			self.agree=0
			self.dis_agree=0
			self.strongly_disagree=0
			

	@api.onchange('dis_agree')
	def onchanging_dis_agree(self):
		if self.dis_agree!=0:
			self.strong_agree=0
			self.agree=0
			self.neutral=0
			self.strongly_disagree=0

	@api.onchange('strongly_disagree')
	def onchanging_dis_agree(self):
		if self.dis_agree!=0:
			self.strong_agree=0
			self.agree=0
			self.neutral=0
			self.dis_agree=0
			

class AboutMuslimEnglishLanguageManager(models.Model):
	_name='employee.manager.lines'

	manager=fields.Char(string="Questions")
	strong_agree=fields.Boolean(string="Strongly Agree")
	agree=fields.Boolean(string="Agree")
	neutral=fields.Boolean(string="Neutral")
	dis_agree=fields.Boolean(string="Dis Agree")
	strongly_disagree =fields.Boolean(string="Strongly Disagree")
	reason=fields.Char('Reason for Disagree')
	manager_lines=fields.Many2one('employee.satisfation')
	@api.onchange('strong_agree')
	def onchanging_strong_agree(self):
		if self.strong_agree!=0:
			self.agree=0
			self.neutral=0
			self.dis_agree=0
			self.strongly_disagree=0

	@api.onchange('agree')
	def onchanging_agree(self):
		if self.agree!=0:
			self.strong_agree=0
			self.neutral=0
			self.dis_agree=0
			self.strongly_disagree=0

	@api.onchange('neutral')
	def onchanging_neutral(self):
		if self.neutral!=0:
			self.strong_agree=0
			self.agree=0
			self.dis_agree=0
			self.strongly_disagree=0
			

	@api.onchange('dis_agree')
	def onchanging_dis_agree(self):
		if self.dis_agree!=0:
			self.strong_agree=0
			self.agree=0
			self.neutral=0
			self.strongly_disagree=0

	@api.onchange('strongly_disagree')
	def onchanging_dis_agree(self):
		if self.dis_agree!=0:
			self.strong_agree=0
			self.agree=0
			self.neutral=0
			self.dis_agree=0
			

	

class AboutMuslimEnglishLanguageEnablement(models.Model):
	_name='employee.enablement.lines'

	enablement=fields.Char(string="Questions")
	strong_agree=fields.Boolean(string="Strongly Agree")
	agree=fields.Boolean(string="Agree")
	neutral=fields.Boolean(string="Neutral")
	dis_agree=fields.Boolean(string="Dis Agree")
	strongly_disagree =fields.Boolean(string="Strongly Disagree")
	reason=fields.Char('Reason for Disagree')
	enablement_lines=fields.Many2one('employee.satisfation')
	@api.onchange('strong_agree')
	def onchanging_strong_agree(self):
		if self.strong_agree!=0:
			self.agree=0
			self.neutral=0
			self.dis_agree=0
			self.strongly_disagree=0

	@api.onchange('agree')
	def onchanging_agree(self):
		if self.agree!=0:
			self.strong_agree=0
			self.neutral=0
			self.dis_agree=0
			self.strongly_disagree=0

	@api.onchange('neutral')
	def onchanging_neutral(self):
		if self.neutral!=0:
			self.strong_agree=0
			self.agree=0
			self.dis_agree=0
			self.strongly_disagree=0
			

	@api.onchange('dis_agree')
	def onchanging_dis_agree(self):
		if self.dis_agree!=0:
			self.strong_agree=0
			self.agree=0
			self.neutral=0
			self.strongly_disagree=0

	@api.onchange('strongly_disagree')
	def onchanging_dis_agree(self):
		if self.dis_agree!=0:
			self.strong_agree=0
			self.agree=0
			self.neutral=0
			self.dis_agree=0
			

	

class AboutMuslimEnglishLanguageAlignment(models.Model):
	_name='employee.alignment.lines'

	alignment=fields.Char(string="Questions")
	strong_agree=fields.Boolean(string="Strongly Agree")
	agree=fields.Boolean(string="Agree")
	neutral=fields.Boolean(string="Neutral")
	dis_agree=fields.Boolean(string="Dis Agree")
	strongly_disagree =fields.Boolean(string="Strongly Disagree")
	reason=fields.Char('Reason for Disagree')
	alignment_lines=fields.Many2one('employee.satisfation')
	@api.onchange('strong_agree')
	def onchanging_strong_agree(self):
		if self.strong_agree!=0:
			self.agree=0
			self.neutral=0
			self.dis_agree=0
			self.strongly_disagree=0

	@api.onchange('agree')
	def onchanging_agree(self):
		if self.agree!=0:
			self.strong_agree=0
			self.neutral=0
			self.dis_agree=0
			self.strongly_disagree=0

	@api.onchange('neutral')
	def onchanging_neutral(self):
		if self.neutral!=0:
			self.strong_agree=0
			self.agree=0
			self.dis_agree=0
			self.strongly_disagree=0
			

	@api.onchange('dis_agree')
	def onchanging_dis_agree(self):
		if self.dis_agree!=0:
			self.strong_agree=0
			self.agree=0
			self.neutral=0
			self.strongly_disagree=0

	@api.onchange('strongly_disagree')
	def onchanging_dis_agree(self):
		if self.dis_agree!=0:
			self.strong_agree=0
			self.agree=0
			self.neutral=0
			self.dis_agree=0
			

	

class AboutMuslimEnglishLanguageDevelopment(models.Model):
	_name='employee.developement.lines'

	developement=fields.Char(string="Questions")
	strong_agree=fields.Boolean(string="Strongly Agree")
	agree=fields.Boolean(string="Agree")
	neutral=fields.Boolean(string="Neutral")
	dis_agree=fields.Boolean(string="Dis Agree")
	strongly_disagree =fields.Boolean(string="Strongly Disagree")
	reason=fields.Char('Reason for Disagree')
	developement_lines=fields.Many2one('employee.satisfation')
	@api.onchange('strong_agree')
	def onchanging_strong_agree(self):
		if self.strong_agree!=0:
			self.agree=0
			self.neutral=0
			self.dis_agree=0
			self.strongly_disagree=0

	@api.onchange('agree')
	def onchanging_agree(self):
		if self.agree!=0:
			self.strong_agree=0
			self.neutral=0
			self.dis_agree=0
			self.strongly_disagree=0

	@api.onchange('neutral')
	def onchanging_neutral(self):
		if self.neutral!=0:
			self.strong_agree=0
			self.agree=0
			self.dis_agree=0
			self.strongly_disagree=0
			

	@api.onchange('dis_agree')
	def onchanging_dis_agree(self):
		if self.dis_agree!=0:
			self.strong_agree=0
			self.agree=0
			self.neutral=0
			self.strongly_disagree=0

	@api.onchange('strongly_disagree')
	def onchanging_dis_agree(self):
		if self.dis_agree!=0:
			self.strong_agree=0
			self.agree=0
			self.neutral=0
			self.dis_agree=0
			

	















		



	










