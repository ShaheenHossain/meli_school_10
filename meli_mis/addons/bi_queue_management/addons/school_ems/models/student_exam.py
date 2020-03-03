import xlwt, xlsxwriter
import base64
from odoo.exceptions import ValidationError,UserError
from odoo import fields,api,models,_



class studnet_manual_exam(models.Model):
	_name = "student.manual.exam"
	_description = "Student Report"
	_rec_name = 'class_id'
	_auto = False


	campus_id=fields.Many2one('school.school',string="Campus")
	program_id=fields.Many2one('standard.standard',string="Program")
	course_id=fields.Many2one('standard.semester',string="Course Level")
	room_no=fields.Char(string="Room No")
	class_id=fields.Many2one('school.standard',string="Class",store=True)
	exam_end_date=fields.Date(string="Course End Date")
	shift_id=fields.Many2one('standard.medium',string="Shift")
	exam_id=fields.One2many('student.details.exam','exam_id')
	s_no=fields.Integer(string="S.No")
	state=fields.Selection([('draft','Draft'),('confirm','Sended'),('extended','Extended')],default="draft")


	@api.onchange('class_id')
	def get_details(self):
		if self.class_id:
			self.room_no=self.class_id.division_id.name
			self.exam_end_date=self.class_id.end_date

	@api.onchange('exam_id')
	def _get_s_no(self):
		self.s_no = len(self.exam_id)+1

	@api.multi
	def confirmation_button(self):
		rec=self.env['school.standard'].search([])
		
		# obj=self.env['student.student'].search([('school_id','=',self.campus_id.name),('program_id','=',self.program_id.name),('semester_id','=',self.course_id.name),('medium_id','=',self.shift_id.name)])
		
		for x in rec:
			if x.state=='exam':
				if self.class_id.standard==x.standard:
					x.state='finish'

		for y in self.exam_id:
			y.name.state='alumni'




		self.write({'state':'confirm'})

	


class student_details(models.Model):
	_name='student.details.exam'

	s_no=fields.Integer(string="S.No")
	name=fields.Many2one('student.student',string="Student Name")
	f_name=fields.Char(string="Father Name")
	exam_id=fields.Many2one('student.manual.exam')
	exam_type=fields.Selection([('regular','Regular'),('makeup','MakeUp')],string="Exam Type")
	written=fields.Float(string="Written")
	viva_voice=fields.Float(string="Viva Voice")
	total=fields.Char(string="Total")
	grade=fields.Char(string="Grade")
	remarks=fields.Char(string="Remarks")
	course_level=fields.Char(string="Course Level")


	@api.onchange('name')
	def get_fathername(self):
		if self.name:
			self.f_name=self.name.parent_id
			self.course_level=self.name.semester_id.name

	@api.onchange('written','viva_voice')
	def get_total(self):
		if self.written and self.viva_voice:
			total=int(self.written)+int(self.viva_voice)
			
			total1=total%100
			self.total=str(total%100)+"%"
			rec=self.env['grade.master'].search([('name','=',self.exam_id.program_id.name)])
			for x in rec.grade_ids:
				if float(total1) >= float(x.from_mark) and float(total1) <= float(x.to_mark):
					self.grade=x.grade


			written_total = (self.written/self.name.program_id.written_test)*100
			speaking_total = (self.viva_voice/self.name.program_id.speaking_test)*100
			print self.name.program_id.written_test,"======",written_total



			if written_total >= 50 and speaking_total >= 50:
				self.remarks='Congrats'
			if written_total <= 50 and speaking_total >= 50:
				self.remarks='You have a chance to write exam'
			if written_total >= 50 and speaking_total <= 50:
				self.remarks='You have a chance to write exam'
			if written_total < 50 and speaking_total < 50:
				self.remarks="Repeat Same Semester"
	
	@api.constrains('written','viva_voice')
	def written_test_validation(self):
		if self.written>=70 or self.viva_voice>=30:
			raise UserError(_("Please Enter Written Test Marks Below 70 and Viva Voice Below 30"))



	class student_feedback_filtered(models.Model):
		_name ="student.result.excel"

		classes_id=fields.Many2one('student.manual.exam',string="Class")



		@api.multi
		def generated_excel_report4444(self, record):


			employee_obj = self.env['student.details.exam'].search([('exam_id.class_id.name','=',self.classes_id.class_id.name)])
			workbook = xlwt.Workbook()

			# Style for Excel Report
			style0 = xlwt.easyxf('font:bold True; align: horiz left; pattern: pattern solid, fore_colour white', num_format_str='#,##0.00')
			style1 = xlwt.easyxf('font:bold True, color Yellow , height 400;  borders:top double; align: horiz center; pattern: pattern solid, fore_colour blue;', num_format_str='#,##0.00')
			style2 = xlwt.easyxf('font:bold True, color White , height 440;  borders:top double; align: horiz center; pattern: pattern solid, fore_colour  gold;', num_format_str='#,##0.00')
			styletitle = xlwt.easyxf(
							'font:bold True, color White, height 240;  borders: top double; align: horiz center; pattern: pattern solid, fore_colour gold;',
			num_format_str='#,##0.00')
			styletitle1 = xlwt.easyxf(
							'font:bold True, color White, height 240;  borders: top double; align: horiz center; pattern: pattern solid, fore_colour red;',
			num_format_str='#,##0.00')
			sheet = workbook.add_sheet("Student Feedback Report")
			sheet.write_merge(0, 0, 0, 3, 'Student  Results Details', styletitle1)

			sheet.write(1, 0, 'S.No', styletitle)
			sheet.write(1, 1, 'Student Name', styletitle)
			sheet.write(1, 2, 'Father Name', styletitle)
			sheet.write(1, 3, 'Student Id', styletitle)
			
			sheet.write(1, 4, 'Written ', styletitle)
			sheet.write(1, 5, 'VivaVoice', styletitle)
			sheet.write(1, 6, 'TOtal', styletitle)
			sheet.write(1, 7, 'Grade', styletitle)
			sheet.write(1, 8, 'Campus',styletitle1)
			sheet.write(1, 9, 'Program',styletitle1)
			sheet.write(1, 10, 'Course Level',styletitle1)
			sheet.write(1, 11, 'Class',styletitle1)
			sheet.write(1, 12, 'Class End Date',styletitle1)
			sheet.write(1, 13, 'Room No',styletitle1)
			
			

			sheet.col(0).width = 700 * (len('S.No') + 1)
			sheet.col(1).width = 700 * (len('Student Name') + 1)
			sheet.col(2).width = 700 * (len('Father Name') + 1)
			sheet.col(3).width = 700 * (len('Student Id') + 1)
			sheet.col(4).width = 700 * (len('written') + 1)
			sheet.col(5).width = 700 * (len('VivaVOice') + 1)
			sheet.col(6).width = 700 * (len('TOtal') + 1)
		
			sheet.col(7).width = 700 * (len('Grade') + 1)
			sheet.col(8).width = 700 * (len('Campus') + 1)
			sheet.col(9).width = 700 * (len('Program') + 1)
			sheet.col(10).width = 700 * (len('Course Level') + 1)
			sheet.col(11).width = 700 * (len('Class') + 1)
			sheet.col(12).width = 700 * (len('Class End Date') + 1)
			sheet.col(13).width = 700 * (len('Room No') + 1)
			
		

			sheet.row(0).height_mismatch = True
			sheet.row(0).height = 256 * 2

			row = 2
			width = 1

			for rec in employee_obj:
				
				sheet.row(width).height = 256 * 2

				sheet.write(row, 0, rec.s_no)
				sheet.write(row, 1, rec.name.name)
				sheet.write(row, 2, rec.f_name)
				sheet.write(row, 3, rec.exam_type)
				sheet.write(row, 4, rec.written)
				sheet.write(row, 5, rec.viva_voice)
				sheet.write(row, 6, rec.total)
				sheet.write(row, 7, rec.grade)
				sheet.write(row, 8, rec.exam_id.campus_id.name)
				sheet.write(row, 9, rec.exam_id.program_id.name)
				sheet.write(row, 10, rec.exam_id.course_id.name)
				sheet.write(row, 11, rec.exam_id.class_id.standard)
				sheet.write(row, 12, rec.exam_id.exam_end_date)
				sheet.write(row, 13, rec.exam_id.room_no)
			
			
				row +=1
				width += 1
			workbook.save('/tmp/employee_info_list.xls')
			result_file = open('/tmp/employee_info_list.xls', 'rb').read()
	
			attachment_id = self.env['wizard.student.details.results'].create({
						'name': 'Student Results' +'.'+'xls',
						'report': base64.encodestring(result_file)
			})

			return {
					'name': _('Notification'),
					'context': self.env.context,
					'view_type': 'form',
					'view_mode': 'form',
					'res_model': 'wizard.student.details.results',
					'res_id': attachment_id.id,
					'data': None,
					'type': 'ir.actions.act_window',
					'target': 'new'
			}
class WizardEmployeeInformationExcelReport1111(models.TransientModel):
    _name = 'wizard.student.details.results'

    name = fields.Char('File Name', size=64)
    report = fields.Binary('Prepared File', filters='.xls', readonly=True)



class program_inherited_view(models.Model):
	_inherit="standard.standard"

	number=fields.Char(string="Serial Number",copy=False, index=True,default=lambda self: _('New'))
	written_test=fields.Integer(string="Written Test")
	speaking_test=fields.Integer(string="Speaking Test")

	
	@api.model
	def create(self, vals):
		if vals.get('number', _('New')) == _('New'):
			vals['number'] = self.env['ir.sequence'].next_by_code('student.program') or _('New')
		result = super(program_inherited_view, self).create(vals)
		return result






				







