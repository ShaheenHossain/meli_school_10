from odoo import fields,models,api,_




class StudentReport(models.TransientModel):
	_name = 'student.admission.report'


	campus=fields.Many2one('school.school',string="Campus",required=True)
	program=fields.Many2one('standard.standard',string="Program",required=True)
	level_id=fields.Many2one('standard.semester',string="Course Level")
	s_date =fields.Date(string="Start Date")
	e_date = fields.Date(string="End Date")
	types=fields.Selection([('general','General'),('paid','Paid'),('unpaid','UnPaid')],string='Report-Type')
	report_id =fields.One2many('student.report.addmission','r_id')
	followup=fields.Integer(string="Followup", compute="calculate_students_list")
	converted=fields.Integer(string="Converted", compute="calculate_students_list")
	terminated=fields.Integer(string="Terminated", compute="calculate_students_list")
	total=fields.Integer(string="Total", compute="calculate_students_list")


	

	@api.depends('types')
	def calculate_students_list(self):

		rec=self.env['student.student'].search([])
		
		if self.types=='general':
			follow_count=0
			paid_count=0
			terminated=0
			for x in rec:
				if self.campus.name == x.school_id.name and self.level_id.name in (x.semester_id.name,False)  and x.admission_date>self.s_date and x.admission_date<=self.e_date:
					if x.state in ('done','invoiced'):
						paid_count+=1
					if x.state in('followup','draft'):
						follow_count+=1
					if x.state=='terminate':
						terminated+=1

			self.followup=follow_count
			self.converted=paid_count
			self.terminated=terminated
			self.total=int(self.followup)+int(self.converted)+int(self.terminated)

		if self.types=='paid':
			self.followup=False
			self.converted=False
			follow_count1=0
			paid_count1=0
			for x in rec:
				if self.campus.name == x.school_id.name and self.level_id.name in (x.semester_id.name,False) and x.admission_date>self.s_date and x.admission_date<=self.e_date:
					if x.state in ('done','invoiced'):
						paid_count1+=1
						
			self.converted=paid_count1
			self.total=int(self.followup)+int(self.converted)+int(self.terminated)

		if self.types=='unpaid':
			self.followup=False
			self.converted=False
			follow_count2=0
			paid_count2=0
			terminated=0
			for x in rec:
				if self.campus.name == x.school_id.name and self.level_id.name in (x.semester_id.name,False) and x.admission_date>self.s_date and x.admission_date<=self.e_date:
					if x.state=='done':
						paid_count2+=1
					if x.state in('followup','draft'):
						follow_count2+=1
					if x.state=='terminate':
						terminated+=1

			self.followup=follow_count2
			self.converted=paid_count2
			self.terminated=terminated
			self.total=int(self.followup)+int(self.converted)+int(self.terminated)

			


	

	@api.multi
	def cancel_button(self):
		return {
		        	'name': 'Message',
		            'type': 'ir.actions.act_window',
		            'view_type': 'form',
		            'view_mode': 'form',
		            'res_model': 'student.admission.report',
		            'target':'inline',
		            }

		

	@api.onchange('types','level_id')
	def get_students_addmission_status(self):
		rec=self.env['student.student'].search([])
		if self.types=='general':
			students=[]
			count=0
			for x in rec:
				if self.campus.name == x.school_id.name and self.level_id.name in (x.semester_id.name,False) and x.admission_date>self.s_date and x.admission_date<=self.e_date:
					count=count+1
					
					values={
							's_no':count,
							'application_no':x.pid,
							'name':x.id,
							'f_name':x.parent_id,
							'mobile':x.mobile,
							'program':x.program_id.name,
							'c_level':x.semester_id.name,
							'email':x.email,
							'campus':x.school_id.name,
							'status':x.state,
							}
					students.append(values)
			self.report_id=students
		if self.types=='paid':
			students=[]
			count=0
			for x in rec:
				if self.campus.name == x.school_id.name and self.level_id.name in (x.semester_id.name,False) and x.admission_date>self.s_date and x.admission_date<=self.e_date and (x.state in ['done','invoiced']):
					count=count+1
					values={
							's_no':count,
							'application_no':x.pid,
							'name':x.id,
							'f_name':x.parent_id,
							'mobile':x.mobile,
							'program':x.program_id.name,
							'c_level':x.semester_id.name,
							'email':x.email,
							'campus':x.school_id.name,
							'status':x.state
							}
					students.append(values)
			self.report_id=students
		if self.types=='unpaid':
			students=[]
			count=0
			for x in rec:
				if self.campus.name == x.school_id.name and self.level_id.name in (x.semester_id.name,False) and x.admission_date>self.s_date and x.admission_date<=self.e_date and x.state=='draft':
					count=count+1
					values={
							's_no':count,
							'application_no':x.pid,
							'name':x.id,
							'f_name':x.parent_id,
							'mobile':x.mobile,
							'program':x.program_id.name,
							'c_level':x.semester_id.name,
							'email':x.email,
							'campus':x.school_id.name,
							'status':x.state
							}
					students.append(values)
			self.report_id=students

	@api.multi
	def get_student_report(self):
		self.ensure_one()
		active_ids = self.env.context.get('active_ids', [])
		datas={
		'ids':active_ids,
		'model': 'student.student',
		'form': self.read()[0]
		}
		return self.env['report'].get_action(self,'school_ems.student_report_template',data=datas)

class Student_Admission_Template(models.AbstractModel):
	_name = 'report.school_ems.student_report_template'


	def get_all_students(self,campus_id,program,level,s_date,e_date,r_type):
		student_records=self.env['student.student'].search([])
		if r_type=='general':
			class_info = {}
			for x in student_records:
				results = []
				if campus_id[1] == x.school_id.name and level[1] in (x.semester_id.name,False):
					print "22222222222222222"
					if x.admission_date>s_date and x.admission_date<e_date:
					
						results.extend([x.pid,x.name,x.parent_id,x.mobile,x.email,x.school_id.name,x.program_id.name,x.semester_id.name,x.state])
					class_info[x.pid]=results
			print class_info,'2222222222222'
			return class_info
		if r_type=='paid':
			class_info = {}
			for x in student_records:
				results = []
				if campus_id[1] == x.school_id.name and level[1] in (x.semester_id.name,False):
					if x.admission_date>s_date and x.admission_date<e_date and (x.state in ['done','invoiced']):
						results.extend([x.pid,x.name,x.parent_id,x.mobile,x.email,x.school_id.name,x.program_id.name,x.semester_id.name,x.state])
					class_info[x.pid]=results
			return class_info
		if r_type=='unpaid':
			class_info = {}
			for x in student_records:
				results = []
				if campus_id[1] == x.school_id.name and level[1] in (x.semester_id.name,False):
					if x.admission_date>s_date and x.admission_date<e_date and x.state=='draft':
						results.extend([x.pid,x.name,x.parent_id,x.mobile,x.email,x.school_id.name,x.program_id.name,x.semester_id.name,x.state])
					class_info[x.pid]=results
			return class_info


	def campus_student_details(self,campus_id,program,level,s_date,e_date,r_type,followup,converted,terminated,total):
		rec = self.env['student.student'].search([])
		student_details = []
		for dts in rec:
			if dts.school_id.name == campus_id[1] and dts.program_id.name == program[1] and  dts.semester_id.name == level[1]:
				student_details.extend([dts.school_id.name,dts.program_id.name,dts.semester_id.name,s_date,e_date,r_type,followup,converted,terminated,total])
		return student_details

	@api.model
	def render_html(self, docids, data=None):
		register_ids = self.env.context.get('active_ids', [])
		campus_id = data['form'].get('campus')
		program = data['form'].get('program')
		level = data['form'].get('level_id')
		s_date=data['form'].get('s_date')
		e_date=data['form'].get('e_date')
		r_type=data['form'].get('types')
		followup=data['form'].get('followup')
		converted=data['form'].get('converted')
		terminated=data['form'].get('terminated')
		total=data['form'].get('total')
		
		get_data = self.get_all_students(campus_id,program,level,s_date,e_date,r_type)
		student_details = self.campus_student_details(campus_id,program,level,s_date,e_date,r_type,followup,converted,terminated,total)
		docargs = {
		'doc_model':'final.results',
		'data': data,
		'docs': student_details,
		'students':get_data,
		}

		return self.env['report'].render('school_ems.student_report_template', docargs)


class StudentAddmissionReport(models.TransientModel):
	_name = 'student.report.addmission'
	s_no =fields.Integer('S.No',readonly=True)
	application_no = fields.Char(string='Appliation No.')
	name = fields.Many2one('student.student',string="Student Name")
	f_name = fields.Char(string="Father Name")
	mobile = fields.Char(string='Mobile')
	email = fields.Char(string='Email')
	campus =fields.Char(string="Campus")
	program =fields.Char(string="Program")
	c_level =fields.Char(string="Semester")
	status =fields.Char(string="Status")
	r_id=fields.Many2one('student.admission.report')

	


