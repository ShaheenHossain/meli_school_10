
import xlwt, xlsxwriter
import base64
from odoo.exceptions import UserError

from odoo import models, fields, api,_


class student_survey_from(models.Model):

	_name='student.survey'

	name=fields.Many2one('student.student',string="Student Name",required=True)
	s_id=fields.Char(string="Student ID No.")
	d_joining=fields.Date(string="Date of Joining")
	course_level=fields.Char(string="Course Level")
	recommands=fields.Html(string='Recommendations')
	student_lines=fields.Many2one('employee.moneter')
	state=fields.Selection([('draft','Draft'),('done','Done')])
	date=fields.Date('Date')
	total_marks=fields.Integer('Total Marks',compute="_compute_marks")
	percentage=fields.Float('Percentage',compute="_compute_marks")

	s_ids=fields.One2many('student.survey.lines','survey_lines')
	term_ids=fields.One2many('student.term.lines','term_lines')
	material_ids=fields.One2many('student.material.lines','matirial_lines')
	employee_ids=fields.One2many('student.employee.lines','employee_lines')
	environment_ids=fields.One2many('student.environment.lines','environment_lines')
	trainer_ids=fields.One2many('student.trainers.lines','trainer_lines')

	
	def _get_course_data(self):
		rec=self.env['survey.questions'].search([])
		courses=[]
		terms=[]
		material=[]
		employee=[]
		environment=[]
		trainer=[]
		for x in rec:
			for y in x.survey_lines_id:
				question_type = dict(x._fields['student_queston'].selection).get(x.student_queston)
				if x.name=='student':
					self.s_ids=False
					self.term_ids=False
					self.material_ids=False
					self.employee_ids=False
					self.environment_ids=False
					self.trainer_ids=False
					if question_type == 'Course Survey':
						courses.append(({'c_survey1':y.question}))
					self.s_ids=courses
					if question_type == 'Classes for the term':
						terms.append(({'term':y.question}))
					self.term_ids=terms
					if question_type == 'Materials':
						material.append(({'material':y.question}))
					self.material_ids=material
					if question_type == 'Employee':
						employee.append(({'employee':y.question}))
					self.employee_ids=employee
					if question_type == 'Campus Environment':
						environment.append(({'environment':y.question}))
					self.environment_ids=environment
					if question_type == 'Trainers':
						trainer.append(({'trainer':y.question}))
					self.trainer_ids=trainer


		
		
	@api.model
	def _compute_marks(self):
		count=0
		total=0
		for x in self.s_ids:
			total+=1
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
		for x in self.term_ids:
			total+=1
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
		for x in self.material_ids:
			total+=1
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

		for x in self.employee_ids:
			total+=1
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
		for x in self.environment_ids:
			total+=1
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

		for x in self.trainer_ids:
			total+=1
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
		self.total_marks=count

		self.percentage=(count*100)/(total*4)
		print self.percentage,'33333333333333333333333'

		
		

	@api.onchange('name')
	def get_student_details(self):
		rec=self.env['student.student'].search([('name','=',self.name.name)])
		for x in rec:
			self.s_id=x.student_code
			self.d_joining=x.admission_date
			self.course_level=x.semester_id.name




	@api.multi
	def student_survey_confirmation(self):
		self.write({'state':'done'})
			

	
class StudentSurveylines(models.Model):
	_name='student.survey.lines'


	c_survey1=fields.Char(string="Description")
	strong_agree=fields.Boolean(string="Strongly Agree")
	agree=fields.Boolean(string="Agree")
	neutral=fields.Boolean(string="Neutral")
	dis_agree=fields.Boolean(string="Dis Agree")
	strongly_disagree =fields.Boolean(string="Strongly Disagree")
	survey_lines=fields.Many2one('student.survey')
	reason=fields.Text('Reason')

	@api.onchange('dis_agree','strongly_disagree')
	def validate_unacceptable(self):
		if self.dis_agree==True or self.strongly_disagree==True:
			raise UserError('Please Write Unacceptable Reason')

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
			

	

class ClassesForTheTerm(models.Model):
	_name='student.term.lines'


	term=fields.Char(string="Description")
	strong_agree=fields.Boolean(string="Strongly Agree")
	agree=fields.Boolean(string="Agree")
	neutral=fields.Boolean(string="Neutral")
	dis_agree=fields.Boolean(string="Dis Agree")
	strongly_disagree =fields.Boolean(string="Strongly Disagree")
	term_lines=fields.Many2one('student.survey')
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
			

	

class StudentMaterialLines(models.Model):
	_name='student.material.lines'


	material=fields.Char(string="Description")
	strong_agree=fields.Boolean(string="Strongly Agree")
	agree=fields.Boolean(string="Agree")
	neutral=fields.Boolean(string="Neutral")
	dis_agree=fields.Boolean(string="Dis Agree")
	strongly_disagree =fields.Boolean(string="Strongly Disagree")
	matirial_lines=fields.Many2one('student.survey')
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
	

class StudentEmployeeLines(models.Model):
	_name='student.employee.lines'


	employee=fields.Char(string="Description")
	strong_agree=fields.Boolean(string="Strongly Agree")
	agree=fields.Boolean(string="Agree")
	neutral=fields.Boolean(string="Neutral")
	dis_agree=fields.Boolean(string="Dis Agree")
	strongly_disagree =fields.Boolean(string="Strongly Disagree")
	employee_lines=fields.Many2one('student.survey')
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
			self.strongly_disagree=0

			



class StudentCampusEnvironment(models.Model):
	_name='student.environment.lines'


	environment=fields.Char(string="Description")
	strong_agree=fields.Boolean(string="Strongly Agree")
	agree=fields.Boolean(string="Agree")
	neutral=fields.Boolean(string="Neutral")
	dis_agree=fields.Boolean(string="Dis Agree")
	strongly_disagree =fields.Boolean(string="Strongly Disagree")
	environment_lines=fields.Many2one('student.survey')
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
			

	


class StudentTrainers(models.Model):
	_name='student.trainers.lines'


	trainer=fields.Char(string="Description")
	strong_agree=fields.Boolean(string="Strongly Agree")
	agree=fields.Boolean(string="Agree")
	neutral=fields.Boolean(string="Neutral")
	dis_agree=fields.Boolean(string="Dis Agree")
	strongly_disagree =fields.Boolean(string="Strongly Disagree")
	trainer_lines=fields.Many2one('student.survey')
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
			



















	










