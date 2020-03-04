
from odoo import fields,api,models,_



class All_Classes_report(models.TransientModel):
	_name = 'student.report'

	campus=fields.Many2one('school.school',string="Campus")
	program=fields.Many2one('standard.standard',string="Program")
	level_id=fields.Many2one('standard.semester',string="Course Level")
	shift_id=fields.Many2one('standard.medium',string="Shift")
	start_date=fields.Date(string='Start Date')
	end_date=fields.Date(string='End Date')
	class_id=fields.Many2one('school.standard',string="Select Your Class")
	multi_class_id=fields.Many2many('school.standard',string='Multiple Classes')
	report_type=fields.Selection([('all','All'),('single','Single'),('multiple','Multiple')],string='Class Type',default='all')
	shift_type=fields.Selection([('all','All'),('single','Single'),('multiple','Multiple')],string='Shift-Type',default='all')
	m_shift=fields.Many2many('standard.medium',string='Shifts')
	code=fields.Char(string='Program-Code')

	@api.onchange('shift_type')
	def changing_shift_type(self):
		if self.shift_type=='all' or self.shift_type=='multiple' or self.shift_type=='single':
			self.shift_id=False
			self.m_shift=False
	@api.onchange('report_type')
	def changing_class_type(self):
		if self.report_type=='all' or self.report_type=='multiple' or self.report_type=='single':
			self.class_id=False
			self.multi_class_id=False
	@api.onchange('program')
	def get_program_code(self):
		if self.program:
			self.code=self.program.code





	@api.multi
	def all_classes_final_report(self):
		self.ensure_one()
		active_ids = self.env.context.get('active_ids', [])
		datas={
		'ids':active_ids,
		'model': 'final.results',
		'form': self.read()[0]
		}
		return self.env['report'].get_action(self,'school_ems.all_classes_reports111',data=datas)



	class studentresults(models.AbstractModel):
		_name = 'report.school_ems.all_classes_reports111'

		def get_students1(self,campus_id,program,s_id,level,class_id,m_class,s_date,e_date,r_type,s_type,m_shift,p_code):
			student_name = self.env['final.results'].search([])
			if p_code == 'TT':
				if s_type == 'single'and r_type == 'all':
					class_info = {}
					for x in student_name:
						pass_students = 0
						fail_students = 0
						if x.campus.name == campus_id[1] and x.program.name == program[1] and  x.shift_id.code==s_id[1] and x.level_id.name == level[1]:
							if s_date <= x.class_id.start_date and e_date >= x.class_id.end_date:
								for y in x.s_ids:
									results = []
									if y.written>=30 and y.speaking>=20:
										pass_students+=1
									if y.written<30 or y.speaking<20:
										fail_students+=1
									results.extend([x.class_id.standard,pass_students,fail_students])
								class_info[x.class_id.standard]=results
					# passed_total=[]
					# failed_total=[]
					# for h,k in class_info.items():
					# 	passed_total.append(k[1])
					# 	failed_total.append(k[2])
					# print sum(passed_total),'77777777777777'
					# print sum(failed_total),'77777777777777'
					return class_info

				if s_type=='multiple' and r_type=='all':
					print "222222222222222222222"
					class_info={}
					for x in student_name:
						pass_students=0
						fail_students=0
						if x.campus.name == campus_id[1] and x.program.name == program[1] and x.level_id.name == level[1]:
							if s_date <= x.class_id.start_date and e_date >= x.class_id.end_date:
								for i in m_shift:
									if x.shift_id.id==i:
										for y in x.s_ids:
											results=[]
											if y.written>=30 and y.speaking>=20:
												pass_students+=1
											if y.written<30 or y.speaking<20:
												fail_students+=1
											results.extend([x.class_id.standard,pass_students,fail_students])
										class_info[x.class_id.standard]=results
					return class_info

				if  s_type=='all' and r_type=='all':
					print "111111111111111111111"
					
					class_info={}
					for x in student_name:
						pass_students=0
						fail_students=0
						print x.campus.name,'----->',campus_id[1]
						print x.program.name,'----->',program[1]
						print x.level_id.name,'----->',level[1]
						if x.campus.name == campus_id[1] and x.program.name == program[1] and x.level_id.name == level[1]:
							print "333333333333333"
							if s_date <= x.class_id.start_date and e_date >= x.class_id.end_date:
								print "2222222222222222222"
								for y in x.s_ids:
									results=[]
									if y.written>=30 and y.speaking>=20:
										pass_students+=1
									if y.written<30 or y.speaking<20:
										fail_students+=1
									results.extend([x.class_id.standard,pass_students,fail_students])
								class_info[x.class_id.standard]=results
					print class_info,'333333333333333333333'
					return class_info
				if s_type=='all' and r_type=='multiple'   :
					print "000000000000000"
					class_info={}
					for x in student_name:
						pass_students=0
						fail_students=0
						for j in m_class:
							if x.class_id.id==j:
								if s_date <= x.class_id.start_date and e_date >= x.class_id.end_date:
									for y in x.s_ids:
										results=[]
										if y.written>=30 and y.speaking>=20:
												pass_students+=1
										if y.written<30 or y.speaking<20:
											fail_students+=1
										results.extend([x.class_id.standard,pass_students,fail_students])
									class_info[x.class_id.standard]=results
					return class_info

				if s_type=='single' and r_type=='multiple'  :
					class_info={}
					for x in student_name:
						pass_students=0
						fail_students=0
						if x.campus.name == campus_id[1] and x.program.name == program[1] and  x.shift_id.code==s_id[1] and x.level_id.name == level[1]:
							if s_date <= x.class_id.start_date and e_date >= x.class_id.end_date:
								for i in m_class:
									if x.class_id.id==i:
										for y in x.s_ids:
											results=[]
											if y.written>=30 and y.speaking>=20:
												pass_students+=1
											if y.written<30 or y.speaking<20:
												fail_students+=1
											results.extend([x.class_id.standard,pass_students,fail_students])
										class_info[x.class_id.standard]=results
					return class_info
				if s_type=='single' and r_type=='single':
					class_info={}
					for x in student_name:
						pass_students=0
						fail_students=0
						if x.class_id.standard==class_id[1]:
							if x.campus.name == campus_id[1] and x.program.name == program[1] and  x.shift_id.code==s_id[1] and x.level_id.name == level[1]:
								if s_date <= x.class_id.start_date and e_date >= x.class_id.end_date:
									for y in x.s_ids:
										results=[]
										if y.written>=30 and y.speaking>=20:
											pass_students+=1
										if y.written<30 or y.speaking<20:
											fail_students+=1
										results.extend([x.class_id.standard,pass_students,fail_students])
									class_info[x.class_id.standard]=results
					return class_info
			if p_code == 'TYD':
				if s_type == 'all' and r_type == 'all':
					class_info = {}
					for x in student_name:
						pass_students = 0
						fail_students = 0
						if x.campus.name == campus_id[1] and x.program.name == program[1] and x.level_id.name == level[1]:
							if s_date <= x.class_id.start_date and e_date >= x.class_id.end_date:
								for y in x.subject_id:
									results = []
									if y.total > 50:
										pass_students += 1
									if y.total < 50:
										fail_students += 1
									results.extend([x.semester_subjects.name,pass_students,fail_students])
								class_info[x.class_id.standard] = results
					print class_info,'-------------------'
					return class_info
				if s_type == 'all' and r_type == 'multiple':
					class_info={}
					for x in student_name:
						pass_students=0
						fail_students=0
						if x.campus.name == campus_id[1] and x.program.name == program[1] and x.level_id.name == level[1]:
							if s_date <= x.class_id.start_date and e_date >= x.class_id.end_date:
								print '888888888888888888888'
								for i in m_class:
									if x.class_id.id==i:
										print '000000000000000'
										for y in x.subject_id:
											results=[]
											if y.total > 50:
												pass_students += 1
											if y.total < 50:
												fail_students += 1
											results.extend([x.semester_subjects.name,pass_students,fail_students])
										class_info[x.semester_subjects.name]=results
					print class_info,'----------------------'
					return class_info

				if (s_type == 'single' and r_type == 'single') or (s_type == 'single' and r_type == 'all'):
					class_info={}
					for x in student_name:
						pass_students=0
						fail_students=0
						if x.campus.name == campus_id[1] and x.program.name == program[1] and x.level_id.name == level[1] and x.shift_id.code==s_id[1]:
							if s_date <= x.class_id.start_date and e_date >= x.class_id.end_date:
								for y in x.subject_id:
									results=[]
									if y.total > 50:
										pass_students += 1
									if y.total < 50:
										fail_students += 1
									results.extend([x.semester_subjects.name,pass_students,fail_students])
								class_info[x.semester_subjects.name]=results
					print class_info,'----------------------'
					return class_info

				if s_type=='single' and r_type=='multiple':
					class_info={}
					for x in student_name:
						pass_students=0
						fail_students=0
						if x.campus.name == campus_id[1] and x.program.name == program[1] and x.level_id.name == level[1] and x.shift_id.code==s_id[1]:
							if s_date <= x.class_id.start_date and e_date >= x.class_id.end_date:
								for y in x.subject_id:
									results=[]
									if y.total > 50:
										pass_students += 1
									if y.total < 50:
										fail_students += 1
									results.extend([x.semester_subjects.name,pass_students,fail_students])
								class_info[x.semester_subjects.name]=results
					return class_info

				if s_type=='multiple' and r_type=='multiple':
					print "66666666666666666"
					class_info={}
					for x in student_name:
						pass_students=0
						fail_students=0
						if x.campus.name == campus_id[1] and x.program.name == program[1] and x.level_id.name == level[1]:
							if s_date <= x.class_id.start_date and e_date >= x.class_id.end_date:
								print "888888888"
								for i in m_shift:
									if x.shift_id.id==i:
										print "99999999999999"
										for j in m_class:
											if x.class_id.id==j:
												print '0000000000000000000'
												for y in x.subject_id:
													results=[]
													if y.total > 50:
														pass_students += 1
													if y.total < 50:
														fail_students += 1
													results.extend([x.semester_subjects.name,pass_students,fail_students])
												class_info[x.semester_subjects.name]=results
					return class_info

				if s_type=='multiple' and r_type=='all':
					class_info={}
					for x in student_name:
						pass_students=0
						fail_students=0
						if x.campus.name == campus_id[1] and x.program.name == program[1] and x.level_id.name == level[1]:
							if s_date <= x.class_id.start_date and e_date >= x.class_id.end_date:
								print "888888888"
								for i in m_shift:
									if x.shift_id.id==i:
										print "99999999999999"
										for y in x.subject_id:
											results=[]
											if y.total > 50:
												pass_students += 1
											if y.total < 50:
												fail_students += 1
											results.extend([x.semester_subjects.name,pass_students,fail_students])
										class_info[x.semester_subjects.name]=results
					return class_info
				if s_type=='multiple' and r_type=='single':
					class_info={}
					for x in student_name:
						pass_students=0
						fail_students=0
						if x.campus.name == campus_id[1] and x.program.name == program[1] and x.level_id.name == level[1]:
							if s_date <= x.class_id.start_date and e_date >= x.class_id.end_date:
								print "888888888"
								for i in m_shift:
									if x.shift_id.id==i and class_id[1]==x.class_id.standard:
										print "99999999999999"
										for y in x.subject_id:
											results=[]
											if y.total > 50:
												pass_students += 1
											if y.total < 50:
												fail_students += 1
											results.extend([x.semester_subjects.name,pass_students,fail_students])
										class_info[x.semester_subjects.name]=results
					return class_info











		def class_finalexamdetails(self,campus_id,program,level,s_id,class_id,p_code):
		
			classes = self.env['final.results'].search([])
			class_details = []
			for dts in classes:
				if dts.campus.name == campus_id[1] and dts.program.name == program[1] and  dts.level_id.name == level[1]:
					class_details.extend([dts.campus.name,dts.program.name,dts.level_id.name,dts.semester_subjects.name,dts.class_id.standard,p_code])
			print class_details,'222222222'
			return class_details
			

		@api.model
		def render_html(self, docids, data=None):
			
			register_ids = self.env.context.get('active_ids', [])
			campus_id = data['form'].get('campus')
			program = data['form'].get('program')
			s_id=data['form'].get('shift_id')
			level = data['form'].get('level_id')
			class_id=data['form'].get('class_id')
			m_class=data['form'].get('multi_class_id')
			s_date=data['form'].get('start_date')
			e_date=data['form'].get('end_date')
			r_type=data['form'].get('report_type')
			s_type=data['form'].get('shift_type')
			m_shift=data['form'].get('m_shift')
			p_code=data['form'].get('code')
			get_data = self.get_students1(campus_id,program,s_id,level,class_id,m_class,s_date,e_date,r_type,s_type,m_shift,p_code)
			class_details = self.class_finalexamdetails(campus_id,program,level,s_id,class_id,p_code)
			docargs = {
			'doc_model':'final.results',
			'data': data,
			'docs': class_details,
			'students':get_data,
			}

			return self.env['report'].render('school_ems.all_classes_reports111', docargs)








