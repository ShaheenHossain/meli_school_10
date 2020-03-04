import datetime
# from datetime import datetime


from odoo import models, fields, api, _

class RelievingRequest(models.Model):
	_name = "hr.relieving.request"

	state = fields.Selection([('new','New'),
							('inprogress','In Progress'),
							('ceo','Waiting for approve'),
							('completed','Approved'),
							('rejected','Rejected')], default="new", string="Status", readonly=True)


	name = fields.Many2one('hr.employee', string="Employee", required=True)
	relieving_type = fields.Selection([('resign','Resignation'),
									('terminate','Terminated'),
									('blacklist','Blacklist'),
									('layoff','Layoff')],string="Relieving Type")
	reporting_manager = fields.Many2one('hr.employee', string="Reporting Manager")
	relieving_date = fields.Date(string="Relieving Date")

	relieving_request = fields.Char(string="Relieving request Created by ")
	relieving_created_date = fields.Date(string="Relieving Created Date")
	campus = fields.Many2one('school.school',string="Campus")
	department = fields.Char(string="Department")


	informed_rm_hr = fields.Boolean(string="Informed RM and HR")
	exit_policy_verification = fields.Boolean(string="Exit Policy Verification")
	notice_period_approved = fields.Boolean(string="Notice Period Approved")
	exit_clearance_form_provided = fields.Boolean(string="Exit Clearance From Provided")
	admin_clearance = fields.Boolean(string="Admin Clearance")
	finance_clearance = fields.Boolean(string="Finance Clearance")
	it_clearance = fields.Boolean(string="IT Clearance")
	exit_clearance_form_received = fields.Boolean(string="Exit Clearance From Received")
	provide_relieving_document = fields.Boolean(string="Provide Relieving Documnent")
	clearance_condi = fields.Boolean(string="Test", default=False)

	email_received = fields.Boolean(string="Email Received")
	remark = fields.Text(string="Remark")


	@api.onchange('name')
	def name_onchange_action(self):
		print "1111111111112222222"
		if self.name:
			rec = self.env['hr.employee'].search([('name','=',self.name.name)])
			self.department=rec.department_id.name
			self.relieving_date=rec.resign_date
			self.relieving_created_date=fields.Date.today()
			self.campus=rec.school_id
			self.reporting_manager = rec.line_manager_id
			self.relieving_request = self.env.user.name
			self.relieving_type = rec.state
			


	@api.multi
	def confirm_action(self):
		self.write({'state':'inprogress'})

	@api.multi
	def send_to_clearance_action(self):
		self.clearance_condi = True
		
	@api.multi
	def reject_action(self):
		self.write({'state': 'rejected'})

	@api.multi
	def send_to_ceo(self):
		self.write({'state':'ceo'})

	@api.multi
	def done_action(self):
		self.write({'state':'completed'})
