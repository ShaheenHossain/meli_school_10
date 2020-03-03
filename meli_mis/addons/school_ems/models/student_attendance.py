from odoo import fields,api,models,_

class student_attendance_inherited(models.Model):
	_inherit="daily.attendance"

	program_id=fields.Many2one('standard.standard',string="Select Program")
	semester_id=fields.Many2one('standard.semester',string="Select Semester")
	shift_id=fields.Many2one('standard.medium',string="Select Shift")
	room_id=fields.Many2one('standard.division',string="Select Room No")


class classwise_attendance_reports(models.TransientModel):
	_name="student.classwise.attendance"


	class_id=fields.Many2one('school.standard',string="Class")
	campus = fields.Many2one('school.school', "Campus Name")
	from_date=fields.Date(string="From Date")
	to_date=fields.Date(string="To Date")


	@api.onchange('class_id')
	def getting_class_dates(self):
		rec=self.env['school.standard'].search([('standard','=',self.class_id.standard)])
		for x in rec:
			if x.school_id.name==self.campus.name:
				self.from_date=x.start_date
				self.to_date=x.end_date



	@api.multi
	def classwise_students_report(self):
		self.ensure_one()
		active_ids = self.env.context.get('active_ids', [])
		datas={
		'ids':active_ids,
		'model': 'student.classwise.attendance',
		'form': self.read()[0]
		}
		return self.env['report'].get_action(self,'school_ems.student_attendance_report11',data=datas)


class employee_payslip(models.AbstractModel):
	_name = 'report.school_ems.student_attendance_report11'

	def get_students(self,class_id,date_from,date_to):
		student_name = self.env['school.standard'].search([('standard','=',str(class_id[1]))])
		
		total_student = {}
		count = 1

		obj = self.env['daily.attendance'].search([])
		for students in student_name.student_ids:
			name = []
			presents = 0
			absents = 0
			total = 0
			for rec in obj:
				if rec.standard_id.standard == str(class_id[1]):
					if rec.date >= date_from and rec.date <= date_to:
						total = total + 1
						for students_attendance in rec.student_ids:
							
							if students.name == students_attendance.stud_id.name:
								if students_attendance.is_present == True:
									presents = presents + 1
								if students_attendance.is_absent == True:
									absents = absents + 1

			name.extend([str(students.student_code),str(students.name),str(students.parent_id),presents,absents,total])
			total_student[count]=name
			count = count + 1
		return total_student

	def class_details(self,class_id):
		classes = self.env['school.standard'].search([])
		class_details = []
		for dts in classes:
			if dts.standard == str(class_id[1]):
				class_details.extend([str(dts.standard_id.name),str(dts.semester_id.name),str(dts.standard),str(dts.medium_id.name),str(dts.start_date),str(dts.end_date)])
		return class_details



	@api.model
	def render_html(self, docids, data=None):
		register_ids = self.env.context.get('active_ids', [])
		date_from = data['form'].get('from_date')
		date_to = data['form'].get('to_date')
		class_id = data['form'].get('class_id')
		get_data = self.get_students(class_id,date_from,date_to)
		class_details = self.class_details(class_id)
	
		docargs = {
		'doc_model':'student.classwise.attendance',
		'data': data,
		'docs': class_details,
		'students':get_data,
		}
		return self.env['report'].render('school_ems.student_attendance_report11', docargs)
