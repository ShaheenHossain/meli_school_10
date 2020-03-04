from odoo.exceptions import UserError,ValidationError
import time
from datetime import datetime, timedelta
from odoo import api,fields,models,_


class ItRequestForm(models.Model):

	_name = "it.request"
	_rec_name="requester"
	_inherit = ['mail.thread', 'ir.needaction_mixin', 'utm.mixin']

	requester=fields.Many2one('hr.employee',string="Requester",track_visibility="onchange")
	campus=fields.Many2one('school.school',string="Campus",compute="_get_requester_details")
	contact=fields.Char(string="Contact No" ,compute="_get_requester_details")
	probelm_type=fields.Selection([('it','IT'),('database','Datebase')],string="Problem Type",required=True)
	designation=fields.Char('Designation',compute="_get_requester_details")
	email=fields.Char(string="Email",compute="_get_requester_details")
	date=fields.Date(string="Date",default=fields.Date.context_today,readonly=True)
	priyority=fields.Selection([('immediate','Immediate'),('high','High'),('medium','Medium'),('low','Low')],string="Priority",required=True)
	description=fields.Text(string="Description",track_visibility="onchange")
	assign_to=fields.Many2one('hr.employee',string="Assign To")
	state=fields.Selection([('draft','Draft'),
							('sent_hod','Sent-HOD'),
							('it','IT-Department Received'),
							('database','Database Department Received'),
							('assign','Assigned'),
							('done','Done')],default="draft")
	hod_note=fields.Text('HOD-Description')
	it_confirmation=fields.Text('Confirmation',track_visibility='always')
	com_date=fields.Date('Completed Date')
	assign_tasks=fields.Char('Assigned Tasks')
	department=fields.Char('Dummy')

	@api.one
	@api.depends('requester','probelm_type')
	def _get_requester_details(self):
		if self.requester:
			self.campus=self.requester.school_id.id
			self.contact=self.requester.mobile_phone
			self.designation=self.requester.job_id.name
			self.email=self.requester.work_email
			# self.department_id=self.requester.department_id.id
		

	@api.multi
	def changing_form_state(self):
		if self.probelm_type=='database':
			self.it_confirmation="Thank You we have received your problem based on the nature of the problem it will be prioritized."
			self.write({'state':'database'})
		else:
			self.write({'state':'sent_hod'})

	@api.multi
	def IT_Confirmation(self):
		self.it_confirmation="Thank You we have received your problem based on the nature of the problem it will be prioritized."
		self.write({'state':'it'})
	@api.multi
	def request_assigning(self):
		self.write({'state':'assign'})
	@api.multi
	def DoneState(self):
		self.it_confirmation="Your problem has been solved Thank You for waiting"
		self.com_date=datetime.now()
		self.write({'state':'done'})

	@api.onchange('assign_to')
	def AssignedTasks(self):
		rec=self.env['it.request'].search([])
		a_count=0
		# c_count=0
		for x in rec:
			if x.assign_to.id==self.assign_to.id and x.state in ('it','database'):
				a_count=a_count+1
			# if x.assign_to.id==self.assign_to.id and x.state=='done':
			# 	c_count=c_count+1
		self.assign_tasks=a_count
		# self.completed_tasks=c_count

	@api.onchange('probelm_type')
	def get_department(self):
		if self.probelm_type:
			if self.probelm_type=='it':
				self.department='IT'
			if self.probelm_type=='database':
				self.department='Database'






			
