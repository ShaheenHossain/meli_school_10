from odoo.exceptions import UserError,ValidationError
from odoo import api,fields,models,_
import requests



class student_midexam_results(models.Model):
	_name = 'student.midexam'
	_rec_name="class_id"

	# @api.model
	# def _default_employee_name(self):
	# 	employee_rec = self.env['school.teacher'].search([('user_id', '=', self.env.uid)], limit=1)
	# 	print employee_rec.id,'00000000000000'
	# 	return employee_rec.id


	campus=fields.Many2one('school.school',string="Campus")
	program=fields.Many2one('standard.standard',string="Program")
	level_id=fields.Many2one('standard.semester',string="Course Level")
	class_id=fields.Many2one('school.standard',string="Class",ondelete='cascade', index=True, copy=False)
	class_ids=fields.Char(string="Class")
	name=fields.Many2one('school.teacher', string="Name", required=True)
	semester_subjects=fields.Many2one('student.subjects',string="Subjects")
	subject_id=fields.One2many('midexam.results','sub123',string="Subjects")


	_sql_constraints = [
    ('unique_scheme_id', 'unique(program,level_id,class_id,semester_subjects)', 'Error! Subject is Already Exist In This Class and Semester'),
    
			]

	@api.onchange('class_id')
	def get_student_list(self):
		self.class_ids=self.class_id.standard
		values = []
		if self.class_id:
			class_ids = self.env['school.standard'].search([])
			for x in class_ids:
				print x.student_ids,'8888888888888'
				if x.standard == self.class_id.standard:
				 	for a_id in x.student_ids:
				 		print "-----------"
				 		values.append(({'students':a_id.id}))
				 	print values,'1111111111111111111111'
				 	self.subject_id = values




			# print "44444444444444444444444"
			# for a_id in class_ids.student_ids:
			# 	print a_id,'22222222222222222222222'
			# 	values.append(({'students':a_id.id}))
			# print values,'99999999999999'
   # 			self.subject_id = values
	
class mid_exam_results(models.Model):
	_name = 'midexam.results'

	students=fields.Many2one('student.student',string="Students Name",readonly=True)
	f_name=fields.Char(string="F/Name",compute="_compute_details")
	written=fields.Integer(string="Written")
	oral=fields.Integer(string="Oral")
	practical=fields.Integer(string="Practical")
	total=fields.Integer(string="Total",compute="_compute_values")
	views=fields.Char(string="Views")
	sub123=fields.Many2one('student.midexam',ondelete="cascade")
	@api.one
	@api.depends('students')
	def _compute_details(self):
		self.f_name=self.students.parent_id

	@api.one
	@api.depends('written','oral','practical')
	def _compute_values(self):

		self.total=int(self.written)+int(self.oral)+int(self.practical)

	@api.onchange('oral')
	def onchange_oral(self):
		
		if self.oral!=0:
			self.practical=0
		
	@api.onchange('practical')
	def onchange_practical(self):
		if self.practical!=0:
			self.oral=0


	@api.constrains('written','oral','practical','total')
	def client_validation_for_midexam(self):
		if int(self.written)>10 or int(self.oral)>10 or int(self.practical)>10:
			raise UserError(_(str(self.students.name)+'Entered Marks Should be Lessthan or Equal To 10 in (Written,Oral,Practical)'))
		if int(self.total)>20 :
			raise UserError(_(str(self.students.name)+' Your Total Marks more than 20 Marks. Please Correct it'))

class final_exam_results(models.Model):
	_name="final.results"
	_rec_name="class_id"
	_inherit = ['mail.thread','ir.needaction_mixin']
	_log_access = True

	@api.model
	def _default_employee_name(self):
		return self.env.user.name

	campus=fields.Many2one('school.school',string="Campus",required=True)
	program=fields.Many2one('standard.standard',string="Program",required=True)
	level_id=fields.Many2one('standard.semester',string="Course Level",required=True)
	class_id=fields.Many2one('school.standard',string="Class",required=True)
	shift_id=fields.Many2one('standard.medium',string="Shift",required=True)
	teacher_name=fields.Char(string="Teacher",default=_default_employee_name,readonly=True)
	semester_subjects=fields.Many2one('student.subjects',string="Subjects",required=True)
	state=fields.Selection([('draft','Draft'),('confirm','Confirm')],default="draft")
	subject_id=fields.One2many('student.finalexam','sub123',string="Subjects")
	s_ids=fields.One2many('talk.talk','f_ids')
	talk_ids=fields.One2many('talk.exam.details','ta_ids')
	pro=fields.Char(string="Subject")
	class_ids=fields.Char(string='Class')

	_sql_constraints = [
    ('unique_scheme_id', 'unique(program,level_id,class_id,semester_subjects,shift_id)', 'Error! Subject is Already Exist In This Class and Semester'),
    
			]





	@api.onchange('program')
	def get_program_name(self):
		if self.program:
			self.pro=self.program.code
	
	@api.onchange('class_id','semester_subjects')
	def get_student_list(self):
		
		
		if self.program.code=='TYD':
			values = []
			if self.class_id:
				class_ids = self.env['school.standard'].search([('standard','=',self.class_id.standard)])
				for a_id in class_ids.student_ids:
					values.append(({'name':a_id.id,'f_name':a_id.parent_id,'program':self.program.name,'campus':self.campus.name,'shift':self.shift_id.name,'level_id':self.level_id.name}))
	   			self.subject_id = values
	   	if self.program.code=='TT':
	   		values = []
			if self.class_id:
				class_ids = self.env['school.standard'].search([('standard','=',self.class_id.standard)])
				for a_id in class_ids.student_ids:
					values.append(({'name':a_id.id,'f_name':a_id.parent_id,'semester_subjects':self.semester_subjects.name,'campus':self.campus.name,'program':self.program.name,'class_id':self.class_id.standard,'shift_id':self.shift_id.name}))
	   			self.s_ids = values


	@api.multi
	def final_confirmation(self):
		rec1=self.env['final.results'].search([])
		rec2=self.env['school.standard'].search([('standard','=',self.class_id.standard)])
		if self.program.code=='TYD':
			var_list = []
			for y in self.subject_id:

				if rec2 :
					ele = {
					's_name': y.name.id,
					'subject':self.semester_subjects.name,
					'm_term':y.midterm,
					'written':y.written,
					'oral':y.oral,
					'practical':y.practical,
					'evalution':y.evaluation,
					'total':y.total,
					'percentage':y.percentage,
					'grade':y.grade,
					'result':y.result,

					}
					var_list.append(ele)
			self.write({'state':'confirm'})
			self.class_ids=self.class_id.standard
			rec2.exam_history = var_list
			
			return {
		        	'name': 'Message',
		            'type': 'ir.actions.act_window',
		            'view_type': 'form',
		            'view_mode': 'form',
		            'res_model': 'custom.pop.message',
		            'target':'new',
		            'context':{'default_name':"Successfully Submitted."} 
		            }

		if self.program.code=='TT':
			var_list1 = []
			for x in self.s_ids:
				if rec2 :
					ele = {
					's_name': x.name.id,
					'subject':self.semester_subjects.name,
					'written':x.written,
					'speaking':x.speaking,
					'total':x.total,
					'percentage':x.percentage,
					'grade':x.grade,
					'result':x.result,

					}
					var_list1.append(ele)
			self.write({'state':'confirm'})
			self.class_ids=self.class_id.standard
			print var_list1,'----------------------'
			rec2.talk_history = var_list1
			return {
		        	'name': 'Message',
		            'type': 'ir.actions.act_window',
		            'view_type': 'form',
		            'view_mode': 'form',
		            'res_model': 'custom.pop.message',
		            'target':'new',
		            'context':{'default_name':"Successfully Submitted."} 
		            }


class talk_talk_exam_details(models.Model):
	_name='talk.exam.details'

	ta_ids=fields.One2many('talk.talk.exam','ta_ids')

	@api.multi
	def makeup_scheduling(self):
		for x in self.ta_ids:
			if x.p_code=='TT':
				return{
				        'type': 'ir.actions.act_window',
				        'name':'Makeup Schedule',
				        'view_mode': 'form',
				        'res_model': 'makeup.schdule',
				        'target': 'current',
				        'view_id': self.env.ref('school_ems.makeup_exam_schedling').id,
				    	} 
			if x.p_code=='TYD':
				return{
				        'type': 'ir.actions.act_window',
				        'name':'TYD Makeup Schedule',
				        'view_mode': 'form',
				        'res_model': 'tyd.makeup.schdule',
				        'target': 'current',
				        'view_id': self.env.ref('school_ems.tyd_makeup_exam_schedling').id,
				    	} 




class Talk_N_Talk_Exam(models.Model):
	_name='talk.talk.exam'

	campus=fields.Char(string='Campus')
	name=fields.Many2one('student.student',string='Student Name')
	program=fields.Many2one('standard.standard',string='Program')
	shift_id=fields.Char(string='Shift')
	class_id=fields.Many2one('school.standard',string='Class')
	p_code=fields.Char(string='Code')
	ta_ids=fields.Many2one('talk.exam.details',ondelete="cascade")




		
class final_student_exam_results(models.Model):
	_name='student.finalexam'

	name=fields.Many2one('student.student',string="Students Name",readonly=True)
	f_name=fields.Char(string="F/Name",compute="_get_student_details")
	midterm=fields.Integer(string="Midterm",compute="_get_student_details")
	written=fields.Integer(string="Written")
	oral=fields.Integer(string="Oral")
	practical=fields.Integer(string="Practical")
	evaluation=fields.Integer(string="Class Participation & Homework",required=True)
	total=fields.Integer(string="Total",compute="_onchange_total")
	percentage=fields.Char(string='Percentage',compute="_onchnage_total11")
	grade=fields.Char(string="Grade",compute="_onchnage_total11")
	result=fields.Char(string="Results",compute="_onchnage_total11")
	semester_subjects=fields.Char(string="Subjects")
	sub123=fields.Many2one('final.results',ondelete="cascade")
	review=fields.Char(string="Review")
	level_id=fields.Char(string="Course Level")
	makeup=fields.Integer(string="Makeup")
	program=fields.Char(string='Program')
	campus=fields.Char(string='Campus')
	shift=fields.Char(string='Shift')
	
	
	@api.one
	@api.depends('midterm')
	def _get_student_details(self):
		self.f_name=self.name.parent_id
		rec=self.env['student.midexam'].search([])
		for x in rec:
			for y in x.subject_id:
				if y.students.student_code==self.name.student_code:
					if x.semester_subjects.name==self.sub123.semester_subjects.name:
						self.midterm=y.total

	@api.one
	@api.depends('written','oral','practical','evaluation','makeup')
	def _onchange_total(self):
		if self.makeup==0:
			self.total=int(self.midterm)+int(self.written)+int(self.oral)+int(self.practical)+int(self.evaluation)
		else:
			self.total=int(self.midterm)+int(self.makeup)+int(self.evaluation)

	@api.one	
	@api.depends('total')
	def _onchnage_total11(self):
		percentage=(int(self.total)%100)
		self.percentage=str(percentage)+'%'
		rec=self.env['grade.master'].search([('name','=',self.name.program_id.name)])
		for x in rec.grade_ids:
			if float(percentage) >= float(x.from_mark) and float(percentage) <= float(x.to_mark):
				self.grade=x.grade
		if percentage>50:
			self.result='Pass'
		if percentage<50:
			self.result='Chance'
		if percentage==0:
			self.result='Absent'
			
	



	@api.constrains('written','oral','practical','total')
	def client_validation_for_finalexam(self):
		if int(self.written)>30 or int(self.oral)>30 or int(self.practical)>30:
			raise UserError(_(str(self.name.name)+'Entered Marks Should be Lessthan or Equal To 30 in (Written,Oral,Practical)'))
		if int(self.total)>100 or int(self.evaluation)>20:
			raise UserError(_(str(self.name.name)+' Your Total Marks more than 100 Marks. Please Correct it'))
	@api.onchange('oral')
	def onchange_finaloral(self):
		if self.oral!=0:
			self.practical=0
		
	@api.onchange('practical')
	def onchange_finalpractical(self):
		if self.practical!=0:
			self.oral=0

	@api.onchange('written')
	def onchange_finalwritten(self):
		if self.written:
			self.semester_subjects=self.sub123.semester_subjects.name

	@api.multi
	def tyd_failed_student_list(self):
		rec=self.env['final.results'].search([])
		students=[]
		for x in rec:
			for y in x.subject_id:
				if y.total<50:
					students.append({'name': y.name.id,
								'campus':x.campus.name,
								'program':x.program.id,
								'class_id':x.class_id.id,
								'shift_id':x.shift_id.name,
								'p_code':x.program.code
								 
									 })
		return {
				'type': 'ir.actions.act_window',
				'res_model': 'talk.exam.details',
				'view_id': self.env.ref('school_ems.talk_form').id,
				
				'view_mode': 'form',
				'target':'inline',
				'context':{
					'default_ta_ids':students,

					}
				}
			

class talk_and_talk_exam_process(models.Model):
	_name='talk.talk'

	name=fields.Many2one('student.student',string="Students Name",readonly=True)
	f_name=fields.Char(string="F/Name",readonly=True)
	written=fields.Integer(string="Written Test",group_operator = False)
	speaking=fields.Integer(string="Speaking Test",group_operator = False)
	total=fields.Integer(string="Total",group_operator = False)
	percentage=fields.Char(string='Percentage',compute="_onchnage_total11")
	grade=fields.Char(string="Grade",compute="_onchnage_total11")
	result=fields.Char(string="Results",compute="_onchnage_total11")
	semester_subjects=fields.Char(string="Subjects")
	f_ids=fields.Many2one('final.results',ondelete="cascade")
	p_written=fields.Integer(string="C-Written",group_operator = False)
	p_speaking=fields.Integer(string="C-Speaking",group_operator = False)
	campus=fields.Char(string="Campus")
	program=fields.Char(string="Program")
	class_id=fields.Char(string="Class")
	shift_id=fields.Char(string="Shift")

	@api.multi
	def failed_student_list(self):
		rec=self.env['final.results'].search([])
		students=[]
		for x in rec:
			for y in x.s_ids:
				if y.written<30 or y.speaking<20:
					students.append({'name': y.name.id,
								'campus':x.campus.name,
								'program':x.program.id,
								'class_id':x.class_id.id,
								'shift_id':x.shift_id.name,
								'p_code':x.program.code
								 
									 })
		print students,'111111111111'
		return {
				'type': 'ir.actions.act_window',
				'res_model': 'talk.exam.details',
				'view_id': self.env.ref('school_ems.talk_form').id,
				
				'view_mode': 'form',
				'target':'inline',
				'context':{
					'default_ta_ids':students,

					}
				}
			

	@api.constrains('total')
	def check_total(self):
		if self.total>100:
			raise UserError('Your total more than 100')


	@api.onchange('written','speaking')
	def calculate_values(self):
		self.total=self.written+self.speaking

	
	@api.one	
	@api.depends('total')
	def _onchnage_total11(self):
		percentage=(int(self.total)%100)
		self.percentage=str(percentage)+'%'
		rec=self.env['grade.master'].search([('name','=',self.name.program_id.name)])
		for x in rec.grade_ids:
			if float(percentage) >= float(x.from_mark) and float(percentage) <= float(x.to_mark):
				self.grade=x.grade

		if self.written >= 30 and self.speaking >= 20:
			if self.p_written == 0 and self.p_speaking == 0:
				self.result = 'PASS'
		if self.written == 0 and self.speaking == 0:
			self.result='Absent'
		if self.p_written >= 30 and self.p_speaking >= 20:
			if self.written<30 or self.speaking<20:
				self.result = 'PASS'
		if self.written<30 or self.speaking<20:
			if self.p_written == 0 and self.p_speaking == 0:
				self.result='Chance'
		# if self.p_written==0 or self.p_speaking==0:



	@api.constrains('written','speaking','total')
	def client_validation_for_finalexam(self):
		if int(self.total)>100 :
			raise UserError(_(str(self.name.name)+' Your Total Marks more than 100 Marks. Please Correct it'))
		if int(self.written)>60 or int(self.speaking)>40:
			raise UserError(_(str(self.name.name)+'Entered Marks Should be Lessthan or Equal To 60 or 40 in (Written,Oral,Practical)'))
		
		
			
class final_exam_report(models.TransientModel):
	_name = 'student.finalreport'

	campus=fields.Many2one('school.school',string="Campus",required=True)
	program=fields.Many2one('standard.standard',string="Program",required=True)
	level_id=fields.Many2one('standard.semester',string="Course Level",required=True)
	class_id=fields.Many2one('school.standard',string="Class",required=True)
	code=fields.Char(string="Code")
	@api.onchange('program')
	def get_code_for_program(self):
		if self.program:
			self.code=self.program.code

	@api.multi
	def student_final_report(self):
		self.ensure_one()
		active_ids = self.env.context.get('active_ids', [])
		datas={
		'ids':active_ids,
		'model': 'final.results',
		'form': self.read()[0]
		}
		return self.env['report'].get_action(self,'school_ems.student_finalexam_report111',data=datas)

class studentresults(models.AbstractModel):
	_name = 'report.school_ems.student_finalexam_report111'

	def get_students1(self,class_id,campus,level,program,p_code):
		student_name = self.env['final.results'].search([('class_id.standard','=',str(program[1]))])
		student=self.env['school.standard'].search([('standard','=',str(program[1]))])
		if p_code=='TYD':
			info={}
			for x in student_name:
				test=[]
				for y in x.subject_id:
					students=[]
					students.extend([y.name.name,y.f_name,y.midterm,y.written,y.oral,y.practical,y.evaluation,y.makeup,y.total,y.percentage,y.grade,y.result,y.name.student_code])
					test.append(students)
				print info,'222222222222222222222'
				info[x.semester_subjects.name]=test
			
			return info
		if p_code=='TT':
			info={}
			for x in student_name:
				
				test=[]
				for y in x.s_ids:
					results=[]
					results.extend([y.name.name,y.f_name,y.written,y.speaking,y.p_written,y.p_speaking,y.total,y.percentage,y.grade,y.result,y.name.student_code])
					test.append(results)

				info[x.semester_subjects.name]=test
			return info



	def class_finalexamdetails(self,program):
		total_students=self.env['school.standard'].search([('standard','=',str(program[1]))])
		t_students=[]
		for x in total_students:
			t_students.append(len(x.student_ids))
		classes = self.env['final.results'].search([])
		class_details = []
		for dts in classes:
			if dts.class_id.standard == str(program[1]):
				class_details.extend([dts.campus.name,dts.program.name,dts.level_id.name,dts.class_id.standard,dts.semester_subjects.name,dts.pro,t_students[0]])
		
		return class_details

	@api.model
	def render_html(self, docids, data=None):
		register_ids = self.env.context.get('active_ids', [])
		campus = data['form'].get('campus')
		program = data['form'].get('program')
		level = data['form'].get('level_id')
		class_id=data['form'].get('class_id')
		p_code=data['form'].get('code')
		get_data = self.get_students1(campus,program,level,class_id,p_code)
		class_details = self.class_finalexamdetails(class_id)
		docargs = {
		'doc_model':'final.results',
		'data': data,
		'docs': class_details,
		'students':get_data,
		}
		return self.env['report'].render('school_ems.student_finalexam_report111', docargs)

class makeupexam(models.Model):
	_name = 'student.makeup'
	_rec_name="program"

	campus=fields.Many2one('school.school',string="Campus",required=True)
	program=fields.Many2one('standard.standard',string="Program",required=True)
	level_id=fields.Many2one('standard.semester',string="Course Level",required=True)
	class_id=fields.Many2one('school.standard',string="Class")
	shift_id=fields.Many2one('standard.medium',string="Shift",required=True)
	subjects=fields.Many2one('student.subjects',string="Subjects",required=True)
	state=fields.Selection([('draft','Draft'),('confirm','Updated')],default='draft')
	info=fields.One2many('student.makeup.process','makeup')
	info1=fields.One2many('talk.makeup','f_ids')
	pro=fields.Char(string='Code')

	@api.onchange('program')
	def get_program_code(self):
		if self.program:
			self.pro=self.program.code

	@api.onchange('subjects')
	def get_student_list(self):
		values = []
		class_ids = self.env['final.results'].search([('level_id','=',self.level_id.name),('campus','=',self.campus.name)])
		rec=self.env['student.student'].search([('semester_id','=',self.level_id.name),('school_id','=',self.campus.name)])
		if self.pro=='TYD':
			for z in rec:
				count=0
				for x in class_ids:
					for y in x.subject_id:
						if y.name.name==z.name:
							if (y.total)<50:
								count+=1
				if count<=2:
					for a in class_ids:
						for b in a.subject_id:
							if a.semester_subjects.name==self.subjects.name:
								if (b.total)<50 and z.name==b.name.name:
									 values.append(({'name':b.name,'f_name':b.f_name,'midterm':b.midterm,'final':(int(b.written)+int(b.oral)+int(b.practical)),'evaluation':b.evaluation}))

			self.info = values

		if self.pro=='TT':
			values=[]
			for z in rec:
				for x in class_ids:
					for y in x.s_ids:
						if y.name.name==z.name:
							if (y.written>=30 and y.speaking<20 and x.semester_subjects.name==self.subjects.name) or (y.written<30 and y.speaking<20 and x.semester_subjects.name==self.subjects.name) or (y.written<30 and y.speaking>=20 and x.semester_subjects.name==self.subjects.name):
								values.append(({'name':y.name,'f_name':y.f_name,'written':y.written,'speaking':y.speaking,'semester_subjects':self.subjects.name}))
								
			self.info1 = values




	
	@api.multi
	def update_student_results(self):
		rec=self.env['student.makeup.process'].search([])
		obj=self.env['student.finalexam'].search([])
		rec2=self.env['school.standard'].search([])
		rec3=self.env['student.examhistory'].search([])
		rec4=self.env['talk.history'].search([])
		if self.pro=='TYD':
			for x in rec:
				if x.total>50:
					for y in obj:
						if x.name.student_code==y.name.student_code and y.sub123.semester_subjects==self.subjects:
							y.makeup=int(x.written)+int(x.oral)+int(x.practical)
							y.review='Makeup Exam Updated'

			for i in self.info:
				for j in rec3:
					if i.name.standard_id.standard==j.s_name.standard_id.standard and i.name.student_code==j.s_name.student_code and self.subjects.name==j.subject:
						j.makeup=int(i.written)+int(i.oral)+int(i.practical)
						j.total=i.total
						j.percentage=i.percentage
						j.result=i.result
						j.grade=i.grade
			self.write({'state':'confirm'})

		if self.pro=='TT':
			t_rec=self.env['talk.makeup'].search([])
			t_obj=self.env['talk.talk'].search([])
			for y in self.info1:
				for x in t_obj:
					if y.name.student_code==x.name.student_code and y.semester_subjects==x.semester_subjects:
						x.p_written=y.written
						x.p_speaking=y.speaking

			for i in t_rec:
				if i.written>=30 and i.speaking>=20:
					for j in t_obj:
						if i.name.student_code==j.name.student_code and j.f_ids.semester_subjects.name==self.subjects.name:
							
							j.speaking=j.speaking
							j.written=j.written
							j.percentage=i.percentage
							j.total=i.total
							j.grade=i.grade


			for i in self.info1:
				for j in rec4:
					for x in t_obj:
						if j.s_name.student_code==x.name.student_code and j.subject==x.semester_subjects and i.name.standard_id.standard==j.s_name.standard_id.standard:
							if j.written<30 or j.speaking<20:
								j.p_written=x.p_written
								j.p_speaking=x.p_speaking
								j.written=x.written
								j.speaking=x.speaking
								j.total=i.total
								j.percentage=i.percentage
								j.result=i.result
								j.grade=i.grade
			self.write({'state':'confirm'})


class makeup_exam_process(models.Model):
	_name="student.makeup.process"

	name=fields.Many2one('student.student',string="Students Name",readonly=True)
	f_name=fields.Char(string="F/Name",readonly=True)
	subject=fields.Char(string="Subject")
	midterm=fields.Integer(string="Midterm",readonly=True)
	final=fields.Integer(string='Final',readonly=True)
	evaluation=fields.Integer(string="Class Evaluation",readonly=True)
	written=fields.Integer(string="Written")
	oral=fields.Integer(string="Oral")
	practical=fields.Integer(string="Practical")
	total=fields.Integer(string="Total")
	percentage=fields.Char(string='Percentage')
	grade=fields.Char(string="Grade",compute="_onchnage_total111")
	result=fields.Char(string="Results",compute="_onchnage_total111")
	semester_subjects=fields.Char(string="Subjects")
	makeup=fields.Many2one('student.makeup',ondelete="cascade")

	@api.onchange('written','oral','practical')
	def getting_total(self):
		self.total=int(self.midterm)+int(self.evaluation)+int(self.written)+int(self.oral)+int(self.practical)

	@api.onchange('oral')
	def onchange_finaloral1(self):
		if self.oral!=0:
			self.practical=0
		
	@api.onchange('practical')
	def onchange_finalpractical1(self):
		if self.practical!=0:
			self.oral=0

	@api.one	
	@api.depends('total')
	def _onchnage_total111(self):
		percentage=(int(self.total)%100)
		self.percentage=str(percentage)+'%'
		rec=self.env['grade.master'].search([('name','=',self.name.program_id.name)])
		for x in rec.grade_ids:
			if float(percentage) >= float(x.from_mark) and float(percentage) <= float(x.to_mark):
				self.grade=x.grade
		if percentage>50:
			self.result='Pass'
		if percentage<50:
			self.result='Fail'


class Talk_Makeup(models.Model):
	_name = 'talk.makeup'

	name=fields.Many2one('student.student',string="Students Name",readonly=True)
	f_name=fields.Char(string="F/Name",readonly=True)
	written=fields.Integer(string="Written Test")
	speaking=fields.Integer(string="Speaking Test")
	total=fields.Integer(string="Total")
	percentage=fields.Char(string='Percentage',compute='_onchnage_total11')
	grade=fields.Char(string="Grade",compute='_onchnage_total11')
	result=fields.Char(string="Results",compute='_onchnage_total11')
	semester_subjects=fields.Char(string="Subjects")
	f_ids=fields.Many2one('student.makeup',ondelete="cascade")


	@api.constrains('total')
	def check_total(self):
		if self.total>100:
			raise UserError('Your total more than 100')


	@api.onchange('written','speaking')
	def calculate_values(self):
		self.total=self.written+self.speaking

	@api.one	
	@api.depends('total')
	def _onchnage_total11(self):
		percentage=(int(self.total)%100)
		self.percentage=str(percentage)+'%'
		rec=self.env['grade.master'].search([('name','=',self.name.program_id.name)])
		for x in rec.grade_ids:
			if float(percentage) >= float(x.from_mark) and float(percentage) <= float(x.to_mark):
				self.grade=x.grade
		if self.written>=30 and self.speaking>=20:
			self.result='Pass'
		else:
			self.result='Fail'
		

class CustomPopMessage(models.TransientModel):
	_name = "custom.pop.message"

	name = fields.Char(string='Message')


class makeup_exam_schduling(models.Model):
	_name='makeup.schdule'

	s_campus=fields.Many2many('school.school',string='Campus')
	program=fields.Many2one('standard.standard',string='Program')
	s_date=fields.Date(string='Exam Date')
	s_time=fields.Char(string='Time')
	venue=fields.Many2one('school.school',string='Venue')

	s_exam=fields.One2many('schdule.makeup','m_exam')

	@api.onchange('s_campus','program','s_date','s_time','venue')
	def get_failed_students_results(self):
		rec=self.env['talk.talk'].search([])
		campuses=[]
		for y in self.s_campus:
			campuses.append(y.name)
			values=[]
			for x in rec:
				if self.program.name==x.program:
					if x.written<30 or x.speaking<20 and x.campus in campuses:
						ele={
							's_name':x.name.id,
							'campus':x.campus,
							's_date':self.s_date,
							's_time':self.s_time,
							'venue':self.venue.id
							}
						values.append(ele)
			self.s_exam=values


class exam_makeup_schduling(models.Model):
	_name="schdule.makeup"


	s_name=fields.Many2one('student.student',string='Student Name')
	campus=fields.Char(string='Campus')
	s_date=fields.Date(string='Exam Date')
	s_time=fields.Char(string='Time')
	venue=fields.Many2one('school.school',string='Venue')
	m_exam=fields.Many2one('makeup.schdule',ondelete="cascade")


class Tyd_Makeup_Schedule(models.Model):
	_name = "tyd.makeup.schdule"

	s_campus=fields.Many2one('school.school',string='Campus')
	program=fields.Many2one('standard.standard',string='Program')
	course_level=fields.Many2one('standard.semester',string='Course Level')
	subjects=fields.Many2many('student.subjects',string='Subjects')
	shift_id=fields.Many2one('standard.medium',string='Shift')
	s_date=fields.Date(string='Exam Date')
	s_time=fields.Char(string='Exam Time')
	s_exam=fields.One2many('tyd.schdule','t_ids')

	@api.onchange('shift_id','subjects','s_date','s_time')
	def get_students(self):
		rec=self.env['student.finalexam'].search([])
		all_subjects=[]
		for y in self.subjects:
			all_subjects.append(y.name)
			values=[]
			for x in rec:
				if self.course_level.name==x.level_id and self.shift_id.name==x.shift:
					if x.total<50 and x.semester_subjects in all_subjects:
						ele={
							's_name':x.name.id,
							'campus':x.campus,
							's_date':self.s_date,
							's_time':self.s_time
							}
						values.append(ele)
			self.s_exam=values






class Tyd_Makeup_Scheduling_Process(models.Model):
	_name = 'tyd.schdule'

	s_name=fields.Many2one('student.student',string='Student Name')
	campus=fields.Char(string='Campus')
	s_date=fields.Date(string='Exam Date')
	s_time=fields.Char(string='Exam Time')
	t_ids=fields.Many2one('tyd.makeup.schdule',ondelete='cascade')







			




















