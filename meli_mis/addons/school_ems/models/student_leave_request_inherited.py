from odoo.exceptions import ValidationError,UserError

from odoo import fields,models,api,_



class student_leave_request_inherited(models.Model):
	_inherit='studentleave.request'
	actual_leaves=fields.Char(string="Allotted Leaves",compute="_get_student_leaves")
	taken_leaves=fields.Char(string="Balance Leaves",compute="_get_student_leaves")
	course_level=fields.Char(string="Course Level",compute="_get_student_leaves")




	@api.depends('student_id')
	def _get_student_leaves(self):
		if self.student_id:
			rec=self.env['studentleave.request'].search([('student_id','=',self.student_id.name),('state','=','approve')])
			obj=self.env['standard.semester'].search([('name','=',self.student_id.semester_id.name)])
			self.course_level=self.student_id.semester_id.name
			days_count = 0
			for x in rec:
				days_count = days_count + x.days

			if self.student_id.gender == 'male':
				for y in obj:
					self.actual_leaves=y.male_leaves
				print days_count,"================================="
				obj1=int(self.actual_leaves)-int(days_count)
				if self.actual_leaves<days_count:
					self.taken_leaves="No Leaves are available"
				else:
					self.taken_leaves=obj1
			
			if self.student_id.gender == 'female':

				for y in obj:
					self.actual_leaves=y.male_leaves
				print days_count,"================================="
				obj1=int(self.actual_leaves)-int(days_count)
				if self.actual_leaves<days_count:
					self.taken_leaves="No Leaves are available"
				else:
					self.taken_leaves=obj1
			
			


	@api.constrains('days')
	def check_student_valid_dates(self):
		
		
		if int(self.taken_leaves) < self.days:
			raise UserError(_('you have only '+self.taken_leaves+'Leaves Only'))






