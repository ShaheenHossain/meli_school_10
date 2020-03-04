from odoo.exceptions import UserError,ValidationError
import time
from datetime import datetime, timedelta
from odoo import api,fields,models,_




class MeetingRequestForm(models.Model):

	_name ="meeting.request"
	_rec_name="requested_by"


	department=fields.Many2one('hr.department',string="department")
	subject=fields.Selection([('meeting','MEETING'),('session','SESSION'),('seminar','SEMINAR'),('workshop','WORKSHOP')],required=True)
	requested_by =fields.Many2one('hr.employee',string="Requested By",required=True)
	purpose_meeting=fields.Char('Purpose Of Meeting',required=True)
	date=fields.Date('Date Of Submission',required=True)
	time =fields.Char('Time')
	designation=fields.Many2one('hr.job','Designation')
	meeting_with =fields.Many2many('hr.employee',string="Meeting With",required=True)
	venue=fields.Char('Venue',required=True)
	state = fields.Selection([('draft','Requester'),('gm','GM'),('schdule','Schduled')],default="draft")
	m_ids=fields.Html("Meeting Agenda",required=True)
	employee_id=fields.One2many('meeting.request.lines','meeting_lines')

	@api.onchange('requested_by')
	def EmployeeDetails(self):
		if self.requested_by:
			self.department=self.requested_by.department_id.id
			self.designation=self.requested_by.job_id.id

	@api.multi
	def GMConfirmation(self):
		self.write({'state':'gm'})

	@api.multi
	def SendToEmployee(self):
		self.write({'state':'schdule'})
		for x in self.employee_id:
			x.state=self.state


	@api.onchange('meeting_with')
	def GetEmployeeDetails(self):
		if self.meeting_with:
			
			employees=[]
			rec=self.env['hr.employee'].search([])
			for x in rec:
				for y in self.meeting_with:
					if x.code==y.code:
						employees.append(({'employee':x.id,'contact':x.mobile_phone,'department':x.department_id.id}))
			self.employee_id=employees
			

				


class MeetingRequestFormLines(models.Model):

	_name = "meeting.request.lines"


	employee = fields.Many2one('hr.employee','Employee')
	contact = fields.Char('Contact')
	status=fields.Selection([('accept','Accepted'),('reject','Rejected')])
	state=fields.Char('State')
	department=fields.Many2one('hr.department',string="department")
	meeting_lines=fields.Many2one('meeting.request')

	@api.multi
	def Confirm(self):
		self.write({'status':'accept'})
		

	@api.multi
	def Reject(self):
		self.write({'status':'reject'})





