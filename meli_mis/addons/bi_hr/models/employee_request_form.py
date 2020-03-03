from odoo.exceptions import UserError
from datetime import datetime


from odoo import models, fields, api,_


class EmployeeRequestForm(models.Model):
	_name = "employee.request.form"

	name = fields.Many2one('hr.employee',string='HoD/AAM Name')
	campus=fields.Many2one('school.school',string='Campus', compute="get_campus_name")
	position=fields.Many2one('hr.employee.category',string='Position/Title')
	department=fields.Many2one('hr.department' ,string="Department")
	no_of_positions=fields.Integer('No. of Open Position')
	expected_start_date=fields.Date('Expected Start Date')
	needs_position=fields.Many2one('hr.job',string='Needs for Position')
	reason_for_opening=fields.Text('Reason For Opening')
	contract_type=fields.Selection([('full_time','Full Time'),
									('part_time','Part Time'),
									('temporary','Temporary(Assignment)'),
									],string='Contract Type')
	english_proficiency=fields.Integer('English Proficiency Requirement',help='Give 1-7 points 1 is min, and 7 is max')
	job_description=fields.Text('Job Description')
	education_preference=fields.Selection([('master','Master'),
											('bachelor','Bachelor'),
											('high_school','High School'),
											('other','Other')],string='Education Preference')
	teacher_analysis=fields.Text('Teacher Statistical Analysis')
	received_date=fields.Date('Request Received Date')
	deadline=fields.Char('Deadline to close the Position')
	prefered_sources=fields.Selection([('internal','Internal'),
										('external','External'),
										('referral','Referral'),
										('all','All')],string='Prefered Sources')
	appicants=fields.Selection([('yes','Yes'),('no','No')],string='Availabity Applicants')
	description=fields.Selection([('yes','Yes (Available)'),
								('no','No (needs to create JD for mentioned position)')],string='Job Description')

	training=fields.Selection([('yes','Yes(Required)'),('no','No')],string='Training')

	state = fields.Selection([('draft','Draft'),
							('hr','HR'),
							('gm','GM'),
							('ceo','CEO'),
							('approve','Approved'),('reject','Rejected')], string="State", default="draft", store=True)

	hr_remark = fields.Text(string="Hr Remark", readonly=True, states={'hr': [('readonly', False)]})
	gm_remark = fields.Text(string="GM Remark", readonly=True, states={'gm': [('readonly', False)]})
	ceo_remark = fields.Text(string="Ceo Remark", readonly=True, states={'ceo': [('readonly', False)]})

	@api.onchange('english_proficiency')
	def onchange_english_proficiency(self):
		if not self.english_proficiency >=1 or self.english_proficiency <= 7:
			raise UserError("Give 1-7 points 1 is Min, and 7 is Max")

	@api.constrains('english_proficiency')
	def english_proficiency_validation(self):
		if not self.english_proficiency >=1 or self.english_proficiency <= 7:
			raise UserError("Give 1-7 points 1 is Min, and 7 is Max")


	@api.constrains('state')
	def remarks_validations(self):
		if self.state == 'gm' or self.state == 'reject':
			if self.hr_remark == False:
				raise UserError("Please write reason for Approve/Reject")
		if self.state == "ceo" or self.state == 'reject':
			if self.gm_remark == False :
				raise UserError('Please write reason for Approve/Reject')
		if self.state == 'approve' or self.state == 'reject':
			if self.ceo_remark == False:
				raise UserError("Please write reason for Approve/Reject")

	@api.depends('name')
	def get_campus_name(self):
		self.campus = self.name.school_id.id


	@api.multi
	def aam_action(self):
		self.write({'state':'hr'})

	@api.multi
	def hr_action(self):
		self.write({'state':'gm'})

	@api.multi
	def gm_action(self):
		self.write({'state':'ceo'})

	@api.multi
	def ceo_action(self):
		self.write({'state':'approve'})

	@api.multi
	def reject_action(self):
		self.write({'state':'reject'})	

