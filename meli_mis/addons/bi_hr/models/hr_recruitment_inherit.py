from odoo import api, fields, models,_


class HrRecruitmentInherit(models.Model):
	_inherit = 'hr.applicant'


	state = fields.Selection([
							('walk_in','Walk-in Profiles'),
							('draft','Shortlisted'),
							('pit','Personal Information Round'),
							('written_test','Written Test'),
							('technical_round','Technical Round'),
							('demo','Demo/AM'),
							('hr_round','Hr Round'),
							('background','Background Verification'),
							('refuse','Refuse'),
							('done','Done')],string='Stages', readonly=True, copy=False, index=True, 
							track_visibility='onchange', default='walk_in')
	current_round = fields.Char(string="Current Round")
	next_round = fields.Char(string="Next Round")

	# PIT information
	total_experience = fields.Float(string="Total Experience")
	current_ctc = fields.Float(string="Current CTC")
	expected_ctc = fields.Float(string="Expected CTC")
	notice_period = fields.Integer(string="Notice Period")
	reason_for_change = fields.Text(string="Reason For Change")
	hr_feedback = fields.Text(string="HR Feedback", readonly=True, states={'pit': [('readonly', False)]})
	# Written test
	written_feedback = fields.Text(string="Written Test Feedback", readonly=True, states={'written_test': [('readonly', False)]})
	# Technical Team Feedback
	strengths = fields.Text(string="Technical Team Feedback", 
							help="""strengths:
							-->
							Weekness:
							-->""", readonly=True, states={'technical_round': [('readonly', False)]})
	Demo_feedback = fields.Text(string="Demo Feedback", readonly=True, states={'demo': [('readonly', False)]})
	# HR Feedback
	salary_disc = fields.Text(string="Salary Discussion", readonly=True, states={'hr_round': [('readonly', False)]})
	# Background Verification.
	employment = fields.Binary(string="Employment", readonly=True, states={'background': [('readonly', False)]})
	employment_name = fields.Char(string="Name", readonly=True, states={'background': [('readonly', False)]})
	employment_status = fields.Selection([('pass','Pass'),('fail','Fail')], string="Employment Status", readonly=True, states={'background': [('readonly', False)]})

	criminal = fields.Binary(string="Criminal Verification", readonly=True, states={'background': [('readonly', False)]})
	criminal_name = fields.Char(string="Name", readonly=True, states={'background': [('readonly', False)]})
	criminal_status = fields.Selection([('pass','Pass'),('fail','Fail')], string="Criminal Status", readonly=True, states={'background': [('readonly', False)]}) 

	salary_verification = fields.Binary(string="Salary Verification", readonly=True, states={'background': [('readonly', False)]})
	salary_name = fields.Char(string="Name", readonly=True, states={'background': [('readonly', False)]})
	salary_verification_status = fields.Selection([('pass','Pass'),('fail','Fail')], string="Salary Status", readonly=True, states={'background': [('readonly', False)]})
	Verification_remark = fields.Text(string="Remark")

	@api.multi
	def walkin_action(self):
		self.write({'state':'draft'})

	@api.multi
	def draft_pit_action(self):
		self.write({'state':'pit'})

	@api.multi
	def pit_written_action(self):
		self.current_round = self.state
		self.write({'state':'written_test'})
		self.next_round = self.state
		self.interview_rounds_email_notification()

	@api.multi
	def written_techncal_action(self):
		self.current_round = self.state
		self.write({'state':'technical_round'})
		self.next_round = self.state
		self.interview_rounds_email_notification()
		
	@api.multi
	def written_demo_action(self):
		self.current_round = self.state
		self.write({'state':'demo'})
		self.next_round = self.state
		self.interview_rounds_email_notification()

		

	@api.multi
	def technical_demo_hr_action(self):
		self.current_round = self.state
		self.write({'state':'hr_round'})
		self.next_round = self.state
		self.interview_rounds_email_notification()
		

	@api.multi
	def hr_done_action(self):
		self.write({'state':'background'})

	@api.multi
	def background_verification_action(self):
		self.write({'state':'done'})



	@api.multi
	def refuse_action(self):
		self.write({'state':'refuse'})

	@api.multi
	def interview_rounds_email_notification(self):
		template = self.env.ref('bi_hr.recruitment_stage_email_template')
		self.env['mail.template'].browse(template.id).send_mail(self.id, force_send=True)
