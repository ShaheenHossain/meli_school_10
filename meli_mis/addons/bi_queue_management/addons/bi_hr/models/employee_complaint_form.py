import datetime
from datetime import datetime
from odoo.exceptions import UserError
import re

from odoo import fields, api,models,_



class employee_complaint_form(models.Model):
	_name = 'hr.employee_complaint'


	@api.model
	def _default_employee_name(self):
		employee_rec = self.env['hr.employee'].search([('user_id', '=', self.env.uid)], limit=1)
		return employee_rec.id


	name=fields.Many2one('hr.employee', string="Name", required=True, default=_default_employee_name, readonly=True)
	email = fields.Char(string="Email", compute="geting_details")
	phone = fields.Char(string="Phone Number", compute="geting_details")
	job_title = fields.Char(string='Current Job Title', compute="geting_details")
	dep = fields.Char(string='Department', compute="geting_details")
	campus_name = fields.Char(string="Campus Name", compute="geting_details")
	work_from =fields.Date(string='How long have you worked for MELI?')
	previous_complaint=fields.Selection([('yes','Yes'),('no','No')],default='no',string="Have you filed an official complaint with any other HOD/AAM earlier?")
	yes_action=fields.Char(string="If YES, with whom was the action commenced?")
	yes_action2=fields.Char(string="At what stage is this action?")
	complaint_discuss=fields.Selection([('yes','Yes'),('no','No')],default='no',string="Have you attempted to resolve this matter by discussing it with someone else?")
	discuss_action1=fields.Char(string="If YES, please provide details:")
	state=fields.Selection([('draft','Draft'),
							('confirm','Confirm'),
							('it','IT'),
							('hr','HR'),
							('gravience','Gravience'),
							('in progress','In Progress'),
							('solved','Solved'),
							('cancel','Cancel'),
							('closed','Closed')],default="draft")
	issue_of_dep=fields.Selection([('hr','HR'),('it','IT'),
							 ('gravience','Gravience')],string="Issue Of Department",required=True)

	name1=fields.Many2one('hr.employee',string="Name",)
	dep1 = fields.Char(string='Department', compute="complaint_name_details")
	title = fields.Char(stiring='Title', compute="complaint_name_details")
	work_location = fields.Char(stiring='Work Location', compute="complaint_name_details")

	remarks = fields.Text(string="Remarks")
	issue_date=fields.Date(string="Compliant-Date",readonly=True)
	solved_date=fields.Date(string='Solved-Date',readonly=True)
	description=fields.Text(string="Reported Issue")

	# it_remarks = fields.Char(string="IT Remarks")
	# gravience_remarks = fields.Char(string="Gravience Remarks")


	assign_to = fields.Many2one('hr.employee',string="Assign To",)
	assign_on = fields.Date('Assigned On')
	status = fields.Char('Status')
	planned_date=fields.Date('Planned Date',readonly=True)
	estimated_time = fields.Date('Estimated Closure Time/Date',readonly=True)
	issue_description=fields.Text('Issue Description')

	@api.depends('name1')
	def complaint_name_details(self):
		if self.name1:
			self.dep1 = self.name1.department_id.name
			self.title = self.name1.job_id.name
			self.work_location = self.name1.school_id.name



	
	@api.one
	@api.depends('name')
	def geting_details(self):
		if self.name:
			self.email=self.name.work_email
			self.phone=self.name.mobile_phone
			self.job_title=self.name.job_id.name
			self.dep=self.name.department_id.name
			self.campus_name = self.name.school_id.name


	@api.multi
	def send_to_hr(self):
		self.issue_date=datetime.now()
		self.write({'state':'hr'})

	@api.multi
	def send_to_it(self):
		self.issue_date=datetime.now()
		self.write({'state':'it'})

	@api.multi
	def send_to_gravience(self):
		self.issue_date=datetime.now()
		self.write({'state':'gravience'})


	@api.multi
	def solved(self):
		self.planned_date=datetime.now()
		self.status='In Process'
		self.write({'state':'in progress'})

		# if self.status=='hr':
		# 	self.write({'status':'in progress'})
		# if self.status=='it':
		# 	self.write({'status':'in progress'})
		# if self.status=='gravience':
		# 	self.write({'status':'in progress'})


	@api.multi
	def confirmation_complaint(self):
		self.write({'state':'confirm'})

	@api.multi
	def complaint_solution(self):
		self.solved_date=datetime.now()
		self.status='Solved'
		self.estimated_time=datetime.now()
		self.write({'state':'solved'})

	@api.multi
	def closed_complaints(self):
		self.write({'state':'closed'})
	@api.multi
	def cancel(self):
		self.write({'state':'cancel'})


	

	



