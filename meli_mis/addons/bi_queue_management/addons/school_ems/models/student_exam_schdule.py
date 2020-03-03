from datetime import date,time
from odoo import fields,api,models,_
import requests
import ast



class student_exam_schdule(models.Model):
	_name = "student.schdule"
	_rec_name="program"


	campus_id=fields.Many2one('school.school',string="Campus")
	program=fields.Many2one('standard.standard',string="Program")
	semester=fields.Many2one('standard.semester',string="Course Level")
	shift_id=fields.Many2one('standard.medium',string="Shift")
	class_id=fields.Many2one('school.standard',string='Class')
	mid_class_id=fields.Many2one('school.standard',string='Class')
	s_date=fields.Date(string='Start Date')
	e_date=fields.Date(string='End Date')
	schdule_date=fields.Date(string='Schdule Date',readonly=True,default=date.today())
	
	subjects=fields.Many2one('student.subjects',string='Subject')
	state=fields.Selection([('draft','Draft'),('confirm','Confirmed')],default='draft')
	exam_type=fields.Selection([('mid_exam','Mid-Exam'),('final_exam','Final-Exam')],default='mid_exam',string='Exam-Type')
	suchdule_id=fields.One2many('student.exam.schdule','suchdule_id',string="Schduling")
	d_class_id=fields.Char('Class')
	
	_sql_constraints = [
    ('unique_scheme_id1', 'unique(mid_class_id,class_id)', 'Error! Already This class Was Schduled'),
    
			]

	



	@api.onchange('class_id','semester','mid_class_id')
	def get_class_dates(self):
		print "99999999999999999"
		if self.class_id:
			# self.s_date=self.class_id.start_date
			# self.e_date=self.class_id.end_date
			rec=self.env['student.subjects'].search([('semester_id','=',self.semester.name)])
			values=[]
			for x in rec:
				ele={
				'name':x.name,
				'course_level':self.semester.name,
				'class_id':self.class_id.standard,
				'exam_type':self.exam_type

				}
				values.append(ele)
			self.suchdule_id=values

		if self.mid_class_id:
			self.s_date=self.mid_class_id.start_date
			self.e_date=self.mid_class_id.end_date
			rec=self.env['student.subjects'].search([('semester_id','=',self.semester.name)])
			values=[]
			for x in rec:
				ele={
				'name':x.name,
				'course_level':self.semester.name,
				'class_id':self.class_id.standard,
				'exam_type':self.exam_type

				}
				values.append(ele)
			print values,'00000000000000000'

			self.suchdule_id=values



	@api.multi
	def exam_confirmation(self):
		if self.class_id :
			self.d_class_id=self.class_id.standard
			self.write({'state':'confirm'})
		if self.mid_class_id:
			self.d_class_id=self.mid_class_id.standard
			self.write({'state':'confirm'})

		




	



class student_exam_child(models.Model):
	_name ='student.exam.schdule'


	
	name=fields.Char(string='Subject')
	start_date = fields.Date('Start Date')
	end_date = fields.Date('End Date')
	exam_schdule_date=fields.Date('Exam Schdule Date')
	suchdule_id=fields.Many2one('student.schdule',string="Exam Schduling",ondelete="cascade")
	time=fields.Char(string="Exam Start Time")
	student=fields.Many2one('student.student')
	confirm_exam=fields.Boolean(string='Active')
	course_level=fields.Char(string='Course Level')
	exam_type=fields.Char(string='Exam-Type')
	class_id=fields.Char(string='Class')




class student_classes_inherited(models.Model):
	_inherit = 'school.standard'


	exam_date=fields.Char(string="Exam Date")
	exam_time=fields.Char(string="Exam Time")

    

