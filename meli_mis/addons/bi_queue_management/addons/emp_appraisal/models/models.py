# -*- coding: utf-8 -*-
# Developer1

from odoo import models, fields, api, _

class emp_appraisal(models.Model):
    _name = 'hr.emp_appraisal'


    def _get_employee_id(self):
		# assigning the related employee of the logged in user
		employee_rec = self.env['hr.employee'].search([('user_id', '=', self.env.uid)], limit=1)
		return employee_rec.id

    name = fields.Many2one('hr.employee', string = "Employee",required=True, default=_get_employee_id,readonly=True )
    mobile_number = fields.Char(string="Mobile Number", readonly=True, states={'draft': [('readonly', False)]})
    email = fields.Char(string="Email ID", readonly=True, states={'draft': [('readonly', False)]})
    designation = fields.Char(string="Designation", readonly=True, states={'draft': [('readonly', False)]})
    joining_date = fields.Char(string="Date of Join", readonly=True, states={'draft': [('readonly', False)]})
    department = fields.Char(string="Department", readonly=True, states={'draft': [('readonly', False)]})
    campus = fields.Char(string="Campus", readonly=True, states={'draft': [('readonly', False)]})
    requested_date = fields.Char(string="Requested Date", readonly=True, states={'draft': [('readonly', False)]})
    appraisal_deadline = fields.Date(string="Appraisal Deadline", readonly=True, states={'draft': [('readonly', False)]})
    average = fields.Float(string="Average", readonly=True)
    salary = fields.Integer(string="Current Salary", readonly=True, states={'draft': [('readonly', False)]})
    hike = fields.Integer(string="Hike", readonly=True, states={'send_to_ceo': [('readonly', False)]})
    state = fields.Selection([
    				('draft','Draft'),
    				('confirm','Confirm'),
    				('send_to_hr','Hr Approve'),
    				('send_to_ceo','CEO Approve'),
    				('approved','Approved'),
    				('reject',"Reject")],string='Status', readonly=True, copy=False, index=True, track_visibility='onchange', default='draft')


    # Approach To Work
    sys_process = fields.Float(string="System and Process", readonly=True, states={'send_to_hr': [('readonly', False)]})
    follow_instructions = fields.Float(string="Follow Instructions", readonly=True, states={'send_to_hr': [('readonly', False)]})
    adaptable_flexible = fields.Float(string="Adaptable and Flexible", readonly=True, states={'send_to_hr': [('readonly', False)]})
    ability_plan = fields.Float(string="Abilityt to Plan", readonly=True, states={'send_to_hr': [('readonly', False)]})

    # Technical Skills
    job_knowledge = fields.Float(string="Job Knowledge", readonly=True, states={'send_to_hr': [('readonly', False)]})
    handle_work = fields.Float(string="Skill to Handle Work", readonly=True, states={'send_to_hr': [('readonly', False)]})
    learn_skill = fields.Float(string="Learn New Skill", readonly=True, states={'send_to_hr': [('readonly', False)]})

    # Quality Of Work
    accuracy = fields.Float(string="Accuracy", readonly=True, states={'send_to_hr': [('readonly', False)]})
    reliability= fields.Float(string="Reliability", readonly=True, states={'send_to_hr': [('readonly', False)]})
    client_satisfaction = fields.Float(string="Client Satisfaction", readonly=True, states={'send_to_hr': [('readonly', False)]})

    # Handling Targets
    work_competion_on_time = fields.Float(string="Work Completion on Time", readonly=True, states={'send_to_hr': [('readonly', False)]})
    ability_to_work_under_presure = fields.Float(string="Ability to Work Under Presure", readonly=True, states={'send_to_hr': [('readonly', False)]})
    handling_portfolio = fields.Float(string="Handling New Portfolio", readonly=True, states={'send_to_hr': [('readonly', False)]})

    # Interpersonal Skills
    relationship_co_workers = fields.Float(string="Relationship with co-workers", readonly=True, states={'send_to_hr': [('readonly', False)]})
    problem_solving = fields.Float(string="Problem Solving", readonly=True, states={'send_to_hr': [('readonly', False)]})
    decision = fields.Float(string="Decision Making", readonly=True, states={'send_to_hr': [('readonly', False)]})
    time_management = fields.Float(string="Time Management", readonly=True, states={'send_to_hr': [('readonly', False)]})

    # Communication Skills
    oral_written_ex = fields.Float(string="Oral and Written Expression", readonly=True, states={'send_to_hr': [('readonly', False)]})
    sharing_knowledge = fields.Float(string="sharing of Knowledge", readonly=True, states={'send_to_hr': [('readonly', False)]})

    # Develpoment
    seeks_td = fields.Float(string="Seeks T&D", readonly=True, states={'send_to_hr': [('readonly', False)]})
    open_ideas =  fields.Float(string="Open to Ideas", readonly=True, states={'send_to_hr': [('readonly', False)]})

    # Personality
    enthusiastic = fields.Float(string="Enthusiastic", readonly=True, states={'send_to_hr': [('readonly', False)]})
    trustworthy = fields.Float(string="Trustworthy", readonly=True, states={'send_to_hr': [('readonly', False)]})

    # Code of Conduct
    work_place_ettiquttes = fields.Float(string="Work Place Ettiquttes", readonly=True, states={'send_to_hr': [('readonly', False)]})
    punctuality = fields.Float(string="Punctuality", readonly=True, states={'send_to_hr': [('readonly', False)]})
    descipline = fields.Float(string="Descipline", readonly=True, states={'send_to_hr': [('readonly', False)]})
    attendance = fields.Float(string="Attendance", readonly=True, states={'send_to_hr': [('readonly', False)]})

    # Leadership
    team_work = fields.Float(string="Team Work", readonly=True, states={'send_to_hr': [('readonly', False)]})
    team_building = fields.Float(string="Team Building", readonly=True, states={'send_to_hr': [('readonly', False)]})
    stratege_direction = fields.Float(string="New Stratege and Direction", readonly=True, states={'send_to_hr': [('readonly', False)]})
    participation_hr_act = fields.Float(string="Participation in Hr Activities", readonly=True, states={'send_to_hr': [('readonly', False)]})

    @api.multi
    def confirm_action(self):
    	self.write({'state':'confirm'})

    @api.multi
    def send_to_hr(self):
    	self.write({'state':'send_to_hr'})

    @api.multi
    def hr_approve_action(self):
    	self.write({'state':'send_to_ceo'})

    @api.multi
    @api.one
    # @api.onchange('hike')
    def ceo_approve_action(self):

        rec = self.env['hr.contract'].search([('employee_id.name','=',self.name.name)])
        if rec.wage:
            rec.wage = int(rec.wage) + int(self.hike)
    	self.write({'state':'approved'})

    @api.multi
    def rejection_action(self):
		self.write({'state':'reject'})

	

    @api.multi
    def get_average(self):
		approach = self.sys_process+self.follow_instructions+self.adaptable_flexible+self.ability_plan
		technical = self.job_knowledge+self.handle_work+self.learn_skill
		quality_work = self.accuracy+self.reliability+self.client_satisfaction
		handling = self.work_competion_on_time+self.ability_to_work_under_presure+self.handling_portfolio
		interpersonal = self.relationship_co_workers+self.problem_solving+self.decision+self.time_management
		communication = self.oral_written_ex+self.sharing_knowledge
		dev = self.seeks_td+self.open_ideas
		personality = self.enthusiastic+self.trustworthy
		code = self.work_place_ettiquttes+self.punctuality+self.descipline+self.attendance
		leadership = self.team_work+self.team_building+self.stratege_direction+self.participation_hr_act

		self.average = (approach+technical+quality_work+handling+interpersonal+communication+dev+personality+code+leadership)/31
	

    @api.onchange('name')
    @api.depends('name')
    def onchange_employee_id(self):
		if self.name:
			self.mobile_number=self.name.mobile_phone
			self.email=self.name.work_email
			self.joining_date=self.name.date_of_join
			self.designation=self.name.job_id.name
			self.department=self.name.department_id.name
			self.campus=self.name.company_id.name
			self.requested_date = fields.Date.today()
			self.salary = self.name.offered_salary





	