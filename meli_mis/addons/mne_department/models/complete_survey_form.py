from odoo.exceptions import UserError
from datetime import datetime


from odoo import models, fields, api,_



class CompleteSurveyForm(models.Model):

	_name ='complete.survey'


	name=fields.Selection([('student','Student'),('employee','Employee')],string="Survey Type")
	campus=fields.Many2one('school.school',string="Campus")
	program=fields.Many2one('standard.standard',string="Program")
	level_id=fields.Many2one('standard.semester',string="Course Level")
	shift_id=fields.Many2one('standard.medium',string="Shift",required=True)
	class_id=fields.Many2one('school.standard',string="Class",ondelete='cascade', index=True, copy=False)
	date=fields.Date('Date')
	strength=fields.Integer('Strength',)
	survey_student=fields.Integer('Survey Students')
	
	complete_lines=fields.One2many('complete.surveylines','complete_id')
	term_lines=fields.One2many('complete.termlines','complete_term_id')
	complete_material_lines=fields.One2many('complete.materiallines','complete_material_id')
	complete_employee_lines=fields.One2many('complete.employeelines','complete_employee_id')
	complete_environment_lines=fields.One2many('complete.environmentlines','complete_environment_id')
	complete_trainer_lines=fields.One2many('complete.trainerlines','complete_trainer_id')



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
								if self.class_id.standard==j.name.standard_id.standard:
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
								if self.class_id.standard==j.name.standard_id.standard:
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
								if self.class_id.standard==j.name.standard_id.standard:
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
								if self.class_id.standard==j.name.standard_id.standard:
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
								if self.class_id.standard==j.name.standard_id.standard:
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
								if self.class_id.standard==j.name.standard_id.standard:
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





			



