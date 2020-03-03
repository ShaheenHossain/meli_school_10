from odoo.exceptions import UserError
from datetime import datetime


from odoo import models, fields, api,_



class CompleteSurveyForm(models.Model):

	_name ='complete.survey'


	name=fields.Selection([('student','Student'),('employee','Employee')],string="Survey Type")
	campus=fields.Many2one('school.school',string="Campus")
	program=fields.Many2one('standard.standard',string="Program")
	level_id=fields.Many2one('standard.semester',string="Course Level")
	shift_id=fields.Many2one('standard.medium',string="Shift")
	class_id=fields.Many2one('school.standard',string="Class",ondelete='cascade', index=True, copy=False)
	date=fields.Date('Date')
	strength=fields.Integer('Strength',)
	survey_student=fields.Integer('Survey Students')
	survey_employee=fields.Integer('Survey Employees')


	#For Students

	complete_lines=fields.One2many('complete.surveylines','complete_id')
	term_lines=fields.One2many('complete.termlines','complete_term_id')
	complete_material_lines=fields.One2many('complete.materiallines','complete_material_id')
	complete_employee_lines=fields.One2many('complete.employeelines','complete_employee_id')
	complete_environment_lines=fields.One2many('complete.environmentlines','complete_environment_id')
	complete_trainer_lines=fields.One2many('complete.trainerlines','complete_trainer_id')

	#For Employees

	complete_employee_lines_id=fields.One2many('complete.language.lines','language_lines')
	complete_manager_lines_id=fields.One2many('complete.manager.lines','manager_lines')
	complete_enable_lines_id=fields.One2many('complete.enable.lines','enable_lines')
	complete_alignment_lines_id=fields.One2many('complete.alignment.lines','alignment_lines')
	complete_development_lines_id=fields.One2many('complete.development.lines','development_lines')

	@api.onchange('name','campus','date')
	def getting_employee_strength(self):
		rec=self.env['hr.employee'].search([])
		obj=self.env['survey.questions'].search([])
		obj1=self.env['employee.satisfation'].search([])
		rec1=self.env['employee.moneter'].search([])
		if self.name=="employee":
			if self.campus:
				count=0
				for x in rec:
					if self.campus.name==x.school_id.name:
						count+=1
				self.strength=count
				for employee in rec1:
					employees=0
					if self.campus.id==employee.name.id and self.date==employee.date:
						for z in employee.m_line_id:
							if z.state=='done':
								employees=employees+1
						self.survey_employee=employees
				courses=[]
				terms=[]
				material=[]
				employee=[]
				environment=[]
				trainer=[]
				for b in obj:
					for a in b.survey_lines_id:
						question_type = dict(b._fields['employee_question'].selection).get(b.employee_question)
						if question_type=='About Muslim English Language':
							courses.append(({'term':a.question}))
						self.complete_employee_lines_id=courses
						if question_type == 'Manager':
							terms.append(({'term':a.question}))
						self.complete_manager_lines_id=terms
						if question_type == 'Enablement':
							material.append(({'term':a.question}))
						self.complete_enable_lines_id=material
						if question_type == 'Alignment':
							employee.append(({'term':a.question}))
						self.complete_alignment_lines_id=employee
						if question_type == 'Development':
							environment.append(({'term':a.question}))
						self.complete_development_lines_id=environment

				terms={}
				for i in self.complete_employee_lines_id:
					strong_agree=0
					agree=0
					neutral=0
					dis_agree=0
					s_dis_agree=0
					for j in obj1:
						for k in j.language_id:
							if k.term==i.term:
								if self.campus.id==j.campus.id and self.date==j.date:
									list_values=[]
									if k.strong_agree==True:
										strong_agree+=1
									if k.agree==True:
										agree=agree+1
									if k.neutral==True:
										neutral=neutral+1
									if k.dis_agree==True:
										dis_agree=dis_agree+1
									if k.strongly_disagree==True:
										s_dis_agree=s_dis_agree+1
									list_values.extend([strong_agree,agree,neutral,dis_agree,s_dis_agree])
				 					terms[i.term]=list_values
			 	for a in self.complete_employee_lines_id:
					for m,n in terms.items():
						if m==a.term:
					 		a.strong_agree=n[0]
					 		a.agree=n[1]
					 		a.neutral=n[2]
					 		a.disagree=n[3]
					 		a.strongly_disagree=n[4]
					 		
				manager={}
				for p in self.complete_manager_lines_id:
					strong_agree=0
					agree=0
					neutral=0
					dis_agree=0
					strongly_disagree=0
					for j in obj1:
						for k in j.manager_id:
							if k.manager==p.term:
								if self.campus.id==j.campus.id and self.date==j.date:
									list_values=[]
									if k.strong_agree==True:
										strong_agree+=1
									if k.agree==True:
										agree=agree+1
									if k.neutral==True:
										neutral=neutral+1
									if k.dis_agree==True:
										dis_agree=dis_agree+1
									if k.strongly_disagree==True:
										strongly_disagree=strongly_disagree+1
									list_values.extend([strong_agree,agree,neutral,dis_agree,strongly_disagree])
				 					manager[p.term]=list_values
			 	for a in self.complete_manager_lines_id:
					for m,n in manager.items():
						if m==a.term:
					 		a.strong_agree=n[0]
					 		a.agree=n[1]
					 		a.neutral=n[2]
					 		a.disagree=n[3]
					 		a.strongly_disagree=n[4]

				survey_material={}
				for q in self.complete_enable_lines_id:
					strong_agree=0
					agree=0
					neutral=0
					dis_agree=0
					strongly_disagree=0
					for j in obj1:
						for k in j.enablement_id:
							if k.enablement==q.term:
								if self.campus.id==j.campus.id and self.date==j.date:
									list_values=[]
									if k.strong_agree==True:
										strong_agree+=1
									if k.agree==True:
										agree=agree+1
									if k.neutral==True:
										neutral=neutral+1
									if k.dis_agree==True:
										dis_agree=dis_agree+1
									if k.strongly_disagree==True:
										strongly_disagree=strongly_disagree+1
									list_values.extend([strong_agree,agree,neutral,dis_agree,strongly_disagree])
				 					survey_material[q.term]=list_values
			 	for a in self.complete_enable_lines_id:
					for m,n in survey_material.items():
						if m==a.term:
					 		a.strong_agree=n[0]
					 		a.agree=n[1]
					 		a.neutral=n[2]
					 		a.disagree=n[3]
					 		a.strongly_disagree=n[4]

				survey_alignment={}
				for r in self.complete_alignment_lines_id:
					strong_agree=0
					agree=0
					neutral=0
					dis_agree=0
					strongly_disagree=0
					for j in obj1:
						for k in j.alignment_id:
							if k.alignment==r.term:
								if self.campus.id==j.campus.id and self.date==j.date:
									list_values=[]
									if k.strong_agree==True:
										strong_agree+=1
									if k.agree==True:
										agree=agree+1
									if k.neutral==True:
										neutral=neutral+1
									if k.dis_agree==True:
										dis_agree=dis_agree+1
									if k.strongly_disagree==True:
										strongly_disagree=strongly_disagree+1
									list_values.extend([strong_agree,agree,neutral,dis_agree,strongly_disagree])
				 					survey_alignment[r.term]=list_values
				
			 	for a in self.complete_alignment_lines_id:
					for m,n in survey_alignment.items():
						if m==a.term:
					 		a.strong_agree=n[0]
					 		a.agree=n[1]
					 		a.neutral=n[2]
					 		a.disagree=n[3]
					 		a.strongly_disagree=n[4]


				survey_development={}
				for d in self.complete_development_lines_id:
					strong_agree=0
					agree=0
					neutral=0
					dis_agree=0
					strongly_disagree=0
					for j in obj1:
						for k in j.developement_id:
							if k.developement==d.term:
								if self.campus.id==j.campus.id and self.date==j.date:
									list_values=[]
									if k.strong_agree==True:
										strong_agree+=1
									if k.agree==True:
										agree=agree+1
									if k.neutral==True:
										neutral=neutral+1
									if k.dis_agree==True:
										dis_agree=dis_agree+1
									if k.strongly_disagree==True:
										strongly_disagree=strongly_disagree+1
									list_values.extend([strong_agree,agree,neutral,dis_agree,strongly_disagree])
				 					survey_development[d.term]=list_values
				
			 	for a in self.complete_development_lines_id:
					for m,n in survey_development.items():
						if m==a.term:
					 		a.strong_agree=n[0]
					 		a.agree=n[1]
					 		a.neutral=n[2]
					 		a.disagree=n[3]
					 		a.strongly_disagree=n[4]
					 		

	@api.onchange('campus','class_id')
	def get_class_strenth(self):
		if self.name=='student':
			if self.class_id:
				rec=self.env['student.student'].search([])
				rec1=self.env['employee.moneter'].search([])
				obj=self.env['survey.questions'].search([])
				obj1=self.env['student.survey'].search([])
				count=0
				for x in rec:
					if self.class_id.standard==x.standard_id.standard:
						count=count+1
					self.strength=count
				for y in rec1:
					students=0
					if self.class_id.standard==y.class_id.standard :
						for z in y.student_line_id:
							if z.state=='done':
								students=students+1
						self.survey_student=students
				courses=[]
				terms=[]
				material=[]
				employee=[]
				environment=[]
				trainer=[]
				cour_count=0
				term_count=0
				material_count=0
				employee_count=0
				environment_count=0
				trainer_count=0
				for b in obj:
					for a in b.survey_lines_id:
						question_type = dict(b._fields['student_queston'].selection).get(b.student_queston)
						if question_type=='Course Survey':
							cour_count=cour_count+1
							courses.append(({'question':a.question,'s_no':cour_count}))
						self.complete_lines=courses
						if question_type == 'Classes for the term':
							term_count=term_count+1
							terms.append(({'question':a.question,'s_no':term_count}))
						self.term_lines=terms
						if question_type == 'Materials':
							material_count+=1
							material.append(({'question':a.question,'s_no':material_count}))
						self.complete_material_lines=material
						if question_type == 'Employee':
							employee_count+=1
							employee.append(({'question':a.question,'s_no':employee_count}))
						self.complete_employee_lines=employee
						if question_type == 'Campus Environment':
							environment_count+=1
							environment.append(({'question':a.question,'s_no':environment_count}))
						self.complete_environment_lines=environment
						if question_type == 'Trainers':
							trainer_count+=1
							trainer.append(({'question':a.question,'s_no':trainer_count}))
						self.complete_trainer_lines=trainer

				terms={}
				for i in self.complete_lines:
					strong_agree=0
					agree=0
					neutral=0
					dis_agree=0
					strongly_disagree=0
					for j in obj1:
						for k in j.s_ids:
							if k.c_survey1==i.question:
								if self.class_id.standard==j.name.standard_id.standard and self.date==j.date:
									list_values=[]
									if k.strong_agree==True:
										strong_agree+=1
									if k.agree==True:
										agree=agree+1
									if k.neutral==True:
										neutral=neutral+1
									if k.dis_agree==True:
										dis_agree=dis_agree+1
									if k.strongly_disagree==True:
										strongly_disagree=strongly_disagree+1
									list_values.extend([strong_agree,agree,neutral,dis_agree,strongly_disagree])
				 				terms[i.question]=list_values
			 	for a in self.complete_lines:
					for m,n in terms.items():
						if m==a.question:
					 		a.s_agree=n[0]
					 		a.agree=n[1]
					 		a.neutral=n[2]
					 		a.disagree=n[3]
					 		a.strongly_disagree=n[4]
				forms={}
				for p in self.term_lines:
					strong_agree=0
					agree=0
					neutral=0
					dis_agree=0
					strongly_disagree=0
					for j in obj1:
						for k in j.term_ids:
							if k.term==p.question:
								if self.class_id.standard==j.name.standard_id.standard and self.date==j.date:
									list_values=[]
									if k.strong_agree==True:
										strong_agree+=1
									if k.agree==True:
										agree=agree+1
									if k.neutral==True:
										neutral=neutral+1
									if k.dis_agree==True:
										dis_agree=dis_agree+1
									if k.strongly_disagree==True:
										strongly_disagree=strongly_disagree+1
									list_values.extend([strong_agree,agree,neutral,dis_agree,strongly_disagree])
				 				forms[p.question]=list_values
			 	for a in self.term_lines:
					for m,n in forms.items():
						if m==a.question:
					 		a.s_agree=n[0]
					 		a.agree=n[1]
					 		a.neutral=n[2]
					 		a.disagree=n[3]
					 		a.strongly_disagree=n[4]

				survey_material={}
				for q in self.complete_material_lines:
					strong_agree=0
					agree=0
					neutral=0
					dis_agree=0
					strongly_disagree=0
					for j in obj1:
						for k in j.material_ids:
							if k.material==q.question:
								if self.class_id.standard==j.name.standard_id.standard and self.date==j.date:
									list_values=[]
									if k.strong_agree==True:
										strong_agree+=1
									if k.agree==True:
										agree=agree+1
									if k.neutral==True:
										neutral=neutral+1
									if k.dis_agree==True:
										dis_agree=dis_agree+1
									if k.strongly_disagree==True:
										strongly_disagree=strongly_disagree+1
									list_values.extend([strong_agree,agree,neutral,dis_agree,strongly_disagree])
				 				survey_material[q.question]=list_values
				
			 	for a in self.complete_material_lines:
					for m,n in survey_material.items():
						if m==a.question:
					 		a.s_agree=n[0]
					 		a.agree=n[1]
					 		a.neutral=n[2]
					 		a.disagree=n[3]
					 		a.strongly_disagree=n[4]

				survey_employee={}
				for r in self.complete_employee_lines:
					strong_agree=0
					agree=0
					neutral=0
					dis_agree=0
					strongly_disagree=0
					for j in obj1:
						for k in j.employee_ids:
							if k.employee==r.question:
								if self.class_id.standard==j.name.standard_id.standard and self.date==j.date:
									list_values=[]
									if k.strong_agree==True:
										strong_agree+=1
									if k.agree==True:
										agree=agree+1
									if k.neutral==True:
										neutral=neutral+1
									if k.dis_agree==True:
										dis_agree=dis_agree+1
									if k.strongly_disagree==True:
										strongly_disagree=strongly_disagree+1
									list_values.extend([strong_agree,agree,neutral,dis_agree,strongly_disagree])
				 				survey_employee[r.question]=list_values
				
			 	for a in self.complete_employee_lines:
					for m,n in survey_employee.items():
						if m==a.question:
					 		a.s_agree=n[0]
					 		a.agree=n[1]
					 		a.neutral=n[2]
					 		a.disagree=n[3]
					 		a.strongly_disagree=n[4]


				survey_environment={}
				for d in self.complete_environment_lines:
					strong_agree=0
					agree=0
					neutral=0
					dis_agree=0
					strongly_disagree=0
					for j in obj1:
						for k in j.environment_ids:
							if k.environment==d.question:
								if self.class_id.standard==j.name.standard_id.standard and self.date==j.date:
									list_values=[]
									if k.strong_agree==True:
										strong_agree+=1
									if k.agree==True:
										agree=agree+1
									if k.neutral==True:
										neutral=neutral+1
									if k.dis_agree==True:
										dis_agree=dis_agree+1
									if k.strongly_disagree==True:
										strongly_disagree=strongly_disagree+1
									list_values.extend([strong_agree,agree,neutral,dis_agree,strongly_disagree])
				 				survey_environment[d.question]=list_values
				
			 	for a in self.complete_environment_lines:
					for m,n in survey_environment.items():
						if m==a.question:
					 		a.s_agree=n[0]
					 		a.agree=n[1]
					 		a.neutral=n[2]
					 		a.disagree=n[3]
					 		a.strongly_disagree=n[4]

				survey_trainer={}
				for trainee in self.complete_trainer_lines:
					strong_agree=0
					agree=0
					neutral=0
					dis_agree=0
					strongly_disagree=0
					for j in obj1:
						for k in j.trainer_ids:
							if k.trainer==trainee.question:
								if self.class_id.standard==j.name.standard_id.standard and self.date==j.date:
									list_values=[]
									if k.strong_agree==True:
										strong_agree+=1
									if k.agree==True:
										agree=agree+1
									if k.neutral==True:
										neutral=neutral+1
									if k.dis_agree==True:
										dis_agree=dis_agree+1
									if k.strongly_disagree==True:
										strongly_disagree=strongly_disagree+1
									list_values.extend([strong_agree,agree,neutral,dis_agree,strongly_disagree])
				 				survey_trainer[trainee.question]=list_values
				
			 	for a in self.complete_trainer_lines:
					for m,n in survey_trainer.items():
						if m==a.question:
					 		a.s_agree=n[0]
					 		a.agree=n[1]
					 		a.neutral=n[2]
					 		a.disagree=n[3]
					 		a.strongly_disagree=n[4]


					
	class CompleteSurveyFormLines(models.Model):
		_name = 'complete.surveylines'

		s_no=fields.Integer('Serial No.')
		question=fields.Char('Question',readonly=True)
		s_agree=fields.Integer('Strongly Agree',readonly=True)
		agree=fields.Integer('Agree',readonly=True)
		neutral=fields.Integer('Neutral',readonly=True)
		disagree=fields.Integer('Disagree',readonly=True)
		strongly_disagree=fields.Integer('Strongly Disagree',readonly=True)
		percentage=fields.Char('Percentage',compute="_compute_percentage")
		complete_id=fields.Many2one('complete.survey')

		@api.one
		@api.model
		def _compute_percentage(self):
			if self.s_agree >0 or self.agree>0 or self.neutral>0 or self.disagree>0 or self.strongly_disagree>0:
				for x in self.complete_id:
					if self.s_agree>(self.agree or self.neutral or self.disagree or self.strongly_disagree):
						value=(int(self.s_agree*100))/int(x.survey_student)
						self.percentage="Strongly Agree with "+str(value)+' %'
					if self.agree>(self.s_agree or self.neutral or self.disagree or self.strongly_disagree):
						value=(int(self.agree*100))/int(x.survey_student)
						self.percentage="Agree with "+str(value)+' %'

					if self.neutral>(self.s_agree or self.agree or self.disagree or self.strongly_disagree):
						value=(int(self.neutral*100))/int(x.survey_student)
						self.percentage="Neutral with "+str(value)+' %'

					if self.disagree>(self.s_agree or self.agree or self.neutral or self.strongly_disagree):
						value=(int(self.disagree*100))/int(x.survey_student)
						self.percentage="Disagree with "+str(value)+' %'

					if self.strongly_disagree>(self.s_agree or self.agree or self.neutral or self.disagree):
						value=(int(self.strongly_disagree*100))/int(x.survey_student)
						self.percentage="Strongly Disagree with "+str(value)+' %'


	class CompleteClassesForTheTerm(models.Model):
		_name = 'complete.termlines'

		s_no=fields.Integer('Serial No.')
		question=fields.Char('Question')
		s_agree=fields.Integer('Strongly Agree')
		agree=fields.Integer('Agree')
		neutral=fields.Integer('Neutral')
		disagree=fields.Integer('Disagree')
		strongly_disagree=fields.Integer('Strongly Disagree')
		percentage=fields.Char('Percentage',compute="_compute_percentage")
		complete_term_id=fields.Many2one('complete.survey')
		@api.one
		@api.model
		def _compute_percentage(self):
			if self.s_agree >0 or self.agree>0 or self.neutral>0 or self.disagree>0 or self.strongly_disagree>0:
				for x in self.complete_term_id:
					if self.s_agree>(self.agree or self.neutral or self.disagree or self.strongly_disagree):
						value=(int(self.s_agree*100))/int(x.survey_student)
						self.percentage="Strongly Agree with "+str(value)+' %'
					if self.agree>(self.s_agree or self.neutral or self.disagree or self.strongly_disagree):
						value=(int(self.agree*100))/int(x.survey_student)
						self.percentage="Agree with "+str(value)+' %'

					if self.neutral>(self.s_agree or self.agree or self.disagree or self.strongly_disagree):
						value=(int(self.neutral*100))/int(x.survey_student)
						self.percentage="Neutral with "+str(value)+' %'

					if self.disagree>(self.s_agree or self.agree or self.neutral or self.strongly_disagree):
						value=(int(self.disagree*100))/int(x.survey_student)
						self.percentage="Disagree with "+str(value)+' %'

					if self.strongly_disagree>(self.s_agree or self.agree or self.neutral or self.disagree):
						value=(int(self.strongly_disagree*100))/int(x.survey_student)
						self.percentage="Strongly Disagree with "+str(value)+' %'


	class CompleteStudentMaterialLines(models.Model):
		_name = 'complete.materiallines'

		s_no=fields.Integer('Serial No.')
		question=fields.Char('Question')
		s_agree=fields.Integer('Strongly Agree')
		agree=fields.Integer('Agree')
		neutral=fields.Integer('Neutral')
		disagree=fields.Integer('Disagree')
		strongly_disagree=fields.Integer('Strongly Disagree')
		percentage=fields.Char('Percentage',compute="_compute_percentage")
		complete_material_id=fields.Many2one('complete.survey')
		@api.one
		@api.model
		def _compute_percentage(self):
			if self.s_agree >0 or self.agree>0 or self.neutral>0 or self.disagree>0 or self.strongly_disagree>0:
				for x in self.complete_material_id:
					if self.s_agree>(self.agree or self.neutral or self.disagree or self.strongly_disagree):
						value=(int(self.s_agree*100))/int(x.survey_student)
						self.percentage="Strongly Agree with "+str(value)+' %'
					if self.agree>(self.s_agree or self.neutral or self.disagree or self.strongly_disagree):
						value=(int(self.agree*100))/int(x.survey_student)
						self.percentage="Agree with "+str(value)+' %'

					if self.neutral>(self.s_agree or self.agree or self.disagree or self.strongly_disagree):
						value=(int(self.neutral*100))/int(x.survey_student)
						self.percentage="Neutral with "+str(value)+' %'

					if self.disagree>(self.s_agree or self.agree or self.neutral or self.strongly_disagree):
						value=(int(self.disagree*100))/int(x.survey_student)
						self.percentage="Disagree with "+str(value)+' %'

					if self.strongly_disagree>(self.s_agree or self.agree or self.neutral or self.disagree):
						value=(int(self.strongly_disagree*100))/int(x.survey_student)
						self.percentage="Strongly Disagree with "+str(value)+' %'

	class CompleteStudentEmployeeLines(models.Model):
		_name = 'complete.employeelines'

		s_no=fields.Integer('Serial No.')
		question=fields.Char('Question')
		s_agree=fields.Integer('Strongly Agree')
		agree=fields.Integer('Agree')
		neutral=fields.Integer('Neutral')
		disagree=fields.Integer('Disagree')
		strongly_disagree=fields.Integer('Strongly Disagree')
		percentage=fields.Char('Percentage',compute="_compute_percentage")
		complete_employee_id=fields.Many2one('complete.survey')
		@api.one
		@api.model
		def _compute_percentage(self):
			if self.s_agree >0 or self.agree>0 or self.neutral>0 or self.disagree>0 or self.strongly_disagree>0:
				for x in self.complete_employee_id:
					if self.s_agree>(self.agree or self.neutral or self.disagree or self.strongly_disagree):
						value=(int(self.s_agree*100))/int(x.survey_student)
						self.percentage="Strongly Agree with "+str(value)+' %'
					if self.agree>(self.s_agree or self.neutral or self.disagree or self.strongly_disagree):
						value=(int(self.agree*100))/int(x.survey_student)
						self.percentage="Agree with "+str(value)+' %'

					if self.neutral>(self.s_agree or self.agree or self.disagree or self.strongly_disagree):
						value=(int(self.neutral*100))/int(x.survey_student)
						self.percentage="Neutral with "+str(value)+' %'

					if self.disagree>(self.s_agree or self.agree or self.neutral or self.strongly_disagree):
						value=(int(self.disagree*100))/int(x.survey_student)
						self.percentage="Disagree with "+str(value)+' %'

					if self.strongly_disagree>(self.s_agree or self.agree or self.neutral or self.disagree):
						value=(int(self.strongly_disagree*100))/int(x.survey_student)
						self.percentage="Strongly Disagree with "+str(value)+' %'

	class CompleteCampus_EnvironmentLines(models.Model):
		_name = 'complete.environmentlines'

		s_no=fields.Integer('Serial No.')
		question=fields.Char('Question')
		s_agree=fields.Integer('Strongly Agree')
		agree=fields.Integer('Agree')
		neutral=fields.Integer('Neutral')
		disagree=fields.Integer('Disagree')
		strongly_disagree=fields.Integer('Strongly Disagree')
		percentage=fields.Char('Percentage',compute="_compute_percentage")
		complete_environment_id=fields.Many2one('complete.survey')
		@api.one
		@api.model
		def _compute_percentage(self):
			if self.s_agree >0 or self.agree>0 or self.neutral>0 or self.disagree>0 or self.strongly_disagree>0:
				for x in self.complete_environment_id:
					if self.s_agree>(self.agree or self.neutral or self.disagree or self.strongly_disagree):
						value=(int(self.s_agree*100))/int(x.survey_student)
						self.percentage="Strongly Agree with "+str(value)+' %'
					if self.agree>(self.s_agree or self.neutral or self.disagree or self.strongly_disagree):
						value=(int(self.agree*100))/int(x.survey_student)
						self.percentage="Agree with "+str(value)+' %'

					if self.neutral>(self.s_agree or self.agree or self.disagree or self.strongly_disagree):
						value=(int(self.neutral*100))/int(x.survey_student)
						self.percentage="Neutral with "+str(value)+' %'

					if self.disagree>(self.s_agree or self.agree or self.neutral or self.strongly_disagree):
						value=(int(self.disagree*100))/int(x.survey_student)
						self.percentage="Disagree with "+str(value)+' %'

					if self.strongly_disagree>(self.s_agree or self.agree or self.neutral or self.disagree):
						value=(int(self.strongly_disagree*100))/int(x.survey_student)
						self.percentage="Strongly Disagree with "+str(value)+' %'


	class Complete_Trainers(models.Model):
		_name = 'complete.trainerlines'

		s_no=fields.Integer('Serial No.')
		question=fields.Char('Question')
		s_agree=fields.Integer('Strongly Agree')
		agree=fields.Integer('Agree')
		neutral=fields.Integer('Neutral')
		disagree=fields.Integer('Disagree')
		strongly_disagree=fields.Integer('Strongly Disagree')
		percentage=fields.Char('Percentage',compute="_compute_percentage")
		complete_trainer_id=fields.Many2one('complete.survey')

		@api.one
		@api.model
		def _compute_percentage(self):
			if self.s_agree >0 or self.agree>0 or self.neutral>0 or self.disagree>0 or self.strongly_disagree>0:
				for x in self.complete_trainer_id:
					if self.s_agree>(self.agree or self.neutral or self.disagree or self.strongly_disagree):
						value=(int(self.s_agree*100))/int(x.survey_student)
						self.percentage="Strongly Agree with "+str(value)+' %'
					if self.agree>(self.s_agree or self.neutral or self.disagree or self.strongly_disagree):
						value=(int(self.agree*100))/int(x.survey_student)
						self.percentage="Agree with "+str(value)+' %'

					if self.neutral>(self.s_agree or self.agree or self.disagree or self.strongly_disagree):
						value=(int(self.neutral*100))/int(x.survey_student)
						self.percentage="Neutral with "+str(value)+' %'

					if self.disagree>(self.s_agree or self.agree or self.neutral or self.strongly_disagree):
						value=(int(self.disagree*100))/int(x.survey_student)
						self.percentage="Disagree with "+str(value)+' %'

					if self.strongly_disagree>(self.s_agree or self.agree or self.neutral or self.disagree):
						value=(int(self.strongly_disagree*100))/int(x.survey_student)
						self.percentage="Strongly Disagree with "+str(value)+' %'

	#For Employee Survey Form


	class CompleteAboutMuslimEnglishLanguage(models.Model):
		_name='complete.language.lines'

		term=fields.Char(string="Questions")
		strong_agree=fields.Integer(string="Strongly Agree")
		agree=fields.Integer(string="Agree")
		neutral=fields.Integer(string="Neutral")
		dis_agree=fields.Integer(string="Dis Agree")
		strongly_disagree =fields.Integer(string="Strongly Disagree")
		percentage=fields.Char('High Percentage',compute="_compute_percentage")
		language_lines=fields.Many2one('complete.survey')

		@api.one
		@api.model
		def _compute_percentage(self):
			if self.strong_agree >0 or self.agree>0 or self.neutral>0 or self.dis_agree>0 or self.strongly_disagree>0:
				for x in self.language_lines:
					if self.strong_agree>(self.agree or self.neutral or self.dis_agree or self.strongly_disagree):
						value=(int(self.strong_agree*100))/int(x.survey_employee)
						self.percentage="Strongly Agree with "+str(value)+' %'
					if self.agree>(self.strong_agree or self.neutral or self.dis_agree or self.strongly_disagree):
						value=(int(self.agree*100))/int(x.survey_employee)
						self.percentage="Agree with "+str(value)+' %'

					if self.neutral>(self.strong_agree or self.agree or self.dis_agree or self.strongly_disagree):
						value=(int(self.neutral*100))/int(x.survey_employee)
						self.percentage="Neutral with "+str(value)+' %'

					if self.dis_agree>(self.strong_agree or self.agree or self.neutral or self.strongly_disagree):
						value=(int(self.disagree*100))/int(x.survey_employee)
						self.percentage="Disagree with "+str(value)+' %'

					if self.strongly_disagree>(self.strong_agree or self.agree or self.neutral or self.dis_agree):
						value=(int(self.strongly_disagree*100))/int(x.survey_employee)
						self.percentage="Strongly Disagree with "+str(value)+' %'

	class CompleteAboutMuslimEnglishLanguageManager(models.Model):
		_name='complete.manager.lines'

		term=fields.Char(string="Questions")
		strong_agree=fields.Integer(string="Strongly Agree")
		agree=fields.Integer(string="Agree")
		neutral=fields.Integer(string="Neutral")
		dis_agree=fields.Integer(string="Dis Agree")
		strongly_disagree =fields.Integer(string="Strongly Disagree")
		percentage=fields.Char('High Percentage',compute="_compute_percentage")
		manager_lines=fields.Many2one('complete.survey')

		@api.one
		@api.model
		def _compute_percentage(self):
			if self.strong_agree >0 or self.agree>0 or self.neutral>0 or self.dis_agree>0 or self.strongly_disagree>0:
				for x in self.manager_lines:
					if self.strong_agree>(self.agree or self.neutral or self.dis_agree or self.strongly_disagree):
						value=(int(self.strong_agree*100))/int(x.survey_employee)
						self.percentage="Strongly Agree with "+str(value)+' %'
					if self.agree>(self.strong_agree or self.neutral or self.dis_agree or self.strongly_disagree):
						value=(int(self.agree*100))/int(x.survey_employee)
						self.percentage="Agree with "+str(value)+' %'

					if self.neutral>(self.strong_agree or self.agree or self.dis_agree or self.strongly_disagree):
						value=(int(self.neutral*100))/int(x.survey_employee)
						self.percentage="Neutral with "+str(value)+' %'

					if self.dis_agree>(self.strong_agree or self.agree or self.neutral or self.strongly_disagree):
						value=(int(self.disagree*100))/int(x.survey_employee)
						self.percentage="Disagree with "+str(value)+' %'

					if self.strongly_disagree>(self.strong_agree or self.agree or self.neutral or self.dis_agree):
						value=(int(self.strongly_disagree*100))/int(x.survey_employee)
						self.percentage="Strongly Disagree with "+str(value)+' %'

	class CompleteAboutMuslimEnglishLanguageEnablement(models.Model):
		_name='complete.enable.lines'

		term=fields.Char(string="Questions")
		strong_agree=fields.Integer(string="Strongly Agree")
		agree=fields.Integer(string="Agree")
		neutral=fields.Integer(string="Neutral")
		dis_agree=fields.Integer(string="Dis Agree")
		strongly_disagree =fields.Integer(string="Strongly Disagree")
		percentage=fields.Char('High Percentage',compute="_compute_percentage")
		enable_lines=fields.Many2one('complete.survey')

		@api.one
		@api.model
		def _compute_percentage(self):
			if self.strong_agree >0 or self.agree>0 or self.neutral>0 or self.dis_agree>0 or self.strongly_disagree>0:
				for x in self.enable_lines:
					if self.strong_agree>(self.agree or self.neutral or self.dis_agree or self.strongly_disagree):
						value=(int(self.strong_agree*100))/int(x.survey_employee)
						self.percentage="Strongly Agree with "+str(value)+' %'
					if self.agree>(self.strong_agree or self.neutral or self.dis_agree or self.strongly_disagree):
						value=(int(self.agree*100))/int(x.survey_employee)
						self.percentage="Agree with "+str(value)+' %'

					if self.neutral>(self.strong_agree or self.agree or self.dis_agree or self.strongly_disagree):
						value=(int(self.neutral*100))/int(x.survey_employee)
						self.percentage="Neutral with "+str(value)+' %'

					if self.dis_agree>(self.strong_agree or self.agree or self.neutral or self.strongly_disagree):
						value=(int(self.disagree*100))/int(x.survey_employee)
						self.percentage="Disagree with "+str(value)+' %'

					if self.strongly_disagree>(self.strong_agree or self.agree or self.neutral or self.dis_agree):
						value=(int(self.strongly_disagree*100))/int(x.survey_employee)
						self.percentage="Strongly Disagree with "+str(value)+' %'
		

	class CompleteAboutMuslimEnglishLanguageAlignment(models.Model):
		_name='complete.alignment.lines'

		term=fields.Char(string="Questions")
		strong_agree=fields.Integer(string="Strongly Agree")
		agree=fields.Integer(string="Agree")
		neutral=fields.Integer(string="Neutral")
		dis_agree=fields.Integer(string="Dis Agree")
		strongly_disagree =fields.Integer(string="Strongly Disagree")
		percentage=fields.Char('High Percentage',compute="_compute_percentage")
		alignment_lines=fields.Many2one('complete.survey')

		@api.one
		@api.model
		def _compute_percentage(self):
			if self.strong_agree >0 or self.agree>0 or self.neutral>0 or self.dis_agree>0 or self.strongly_disagree>0:
				for x in self.alignment_lines:
					if self.strong_agree>(self.agree or self.neutral or self.dis_agree or self.strongly_disagree):
						value=(int(self.strong_agree*100))/int(x.survey_employee)
						self.percentage="Strongly Agree with "+str(value)+' %'
					if self.agree>(self.strong_agree or self.neutral or self.dis_agree or self.strongly_disagree):
						value=(int(self.agree*100))/int(x.survey_employee)
						self.percentage="Agree with "+str(value)+' %'

					if self.neutral>(self.strong_agree or self.agree or self.dis_agree or self.strongly_disagree):
						value=(int(self.neutral*100))/int(x.survey_employee)
						self.percentage="Neutral with "+str(value)+' %'

					if self.dis_agree>(self.strong_agree or self.agree or self.neutral or self.strongly_disagree):
						value=(int(self.disagree*100))/int(x.survey_employee)
						self.percentage="Disagree with "+str(value)+' %'

					if self.strongly_disagree>(self.strong_agree or self.agree or self.neutral or self.dis_agree):
						value=(int(self.strongly_disagree*100))/int(x.survey_employee)
						self.percentage="Strongly Disagree with "+str(value)+' %'

	class CompleteAboutMuslimEnglishLanguageDevelopment(models.Model):
		_name='complete.development.lines'

		term=fields.Char(string="Questions")
		strong_agree=fields.Integer(string="Strongly Agree")
		agree=fields.Integer(string="Agree")
		neutral=fields.Integer(string="Neutral")
		dis_agree=fields.Integer(string="Dis Agree")
		strongly_disagree =fields.Integer(string="Strongly Disagree")
		percentage=fields.Char('High Percentage',compute="_compute_percentage")
		development_lines=fields.Many2one('complete.survey')


		@api.one
		@api.model
		def _compute_percentage(self):
			if self.strong_agree >0 or self.agree>0 or self.neutral>0 or self.dis_agree>0 or self.strongly_disagree>0:
				for x in self.development_lines:
					if self.strong_agree>(self.agree or self.neutral or self.dis_agree or self.strongly_disagree):
						value=(int(self.strong_agree*100))/int(x.survey_employee)
						self.percentage="Strongly Agree with "+str(value)+' %'
					if self.agree>(self.strong_agree or self.neutral or self.dis_agree or self.strongly_disagree):
						value=(int(self.agree*100))/int(x.survey_employee)
						self.percentage="Agree with "+str(value)+' %'

					if self.neutral>(self.strong_agree or self.agree or self.dis_agree or self.strongly_disagree):
						value=(int(self.neutral*100))/int(x.survey_employee)
						self.percentage="Neutral with "+str(value)+' %'

					if self.dis_agree>(self.strong_agree or self.agree or self.neutral or self.strongly_disagree):
						value=(int(self.disagree*100))/int(x.survey_employee)
						self.percentage="Disagree with "+str(value)+' %'

					if self.strongly_disagree>(self.strong_agree or self.agree or self.neutral or self.dis_agree):
						value=(int(self.strongly_disagree*100))/int(x.survey_employee)
						self.percentage="Strongly Disagree with "+str(value)+' %'


		



			



