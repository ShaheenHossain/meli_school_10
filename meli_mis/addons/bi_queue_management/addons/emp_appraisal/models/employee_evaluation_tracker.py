# -*- coding: utf-8 -*-
# Developer1

from odoo import models, fields, api, _


class HrEmployeeEvaluationTracker(models.Model):
	_name = "hr.employee.evaluation"

	@api.multi
	def _get_employee_id(self):
		# assigning the related employee of the logged in user
		active_ids = self.env.context.get('active_ids')
		rec = self.env['hr.employee'].search([('id','=',active_ids[0])])
		return rec.id





	name = fields.Many2one('hr.employee', string = "Employee", required=True, default=_get_employee_id, readonly=True)
	mobile_number = fields.Char(string="Mobile Number")
	email = fields.Char(string="Email ID")
	designation = fields.Char(string="Designation")
	joining_date = fields.Char(string="Date of Join")
	department = fields.Char(string="Department")
	campus = fields.Char(string="Campus")
	average = fields.Float(string="Average")
	salary = fields.Integer(string="Current Salary")

	# Approach To Work
	sys_process = fields.Float(string="System and Process")
	follow_instructions = fields.Float(string="Follow Instructions")
	adaptable_flexible = fields.Float(string="Adaptable and Flexible")
	ability_plan = fields.Float(string="Abilityt to Plan")

	# Technical Skills
	job_knowledge = fields.Float(string="Job Knowledge")
	handle_work = fields.Float(string="Skill to Handle Work")
	learn_skill = fields.Float(string="Learn New Skill")

	# Quality Of Work
	accuracy = fields.Float(string="Accuracy")
	reliability= fields.Float(string="Reliability")
	client_satisfaction = fields.Float(string="Client Satisfaction")

	# Handling Targets
	work_competion_on_time = fields.Float(string="Work Completion on Time")
	ability_to_work_under_presure = fields.Float(string="Ability to Work Under Presure")
	handling_portfolio = fields.Float(string="Handling New Portfolio")

	# Interpersonal Skills
	relationship_co_workers = fields.Float(string="Relationship with co-workers")
	problem_solving = fields.Float(string="Problem Solving")
	decision = fields.Float(string="Decision Making")
	time_management = fields.Float(string="Time Management")

	# Communication Skills
	oral_written_ex = fields.Float(string="Oral and Written Expression")
	sharing_knowledge = fields.Float(string="sharing of Knowledge")

	# Develpoment
	seeks_td = fields.Float(string="Seeks T&D")
	open_ideas =  fields.Float(string="Open to Ideas")

	# Personality
	enthusiastic = fields.Float(string="Enthusiastic")
	trustworthy = fields.Float(string="Trustworthy")

	# Code of Conduct
	work_place_ettiquttes = fields.Float(string="Work Place Ettiquttes")
	punctuality = fields.Float(string="Punctuality")
	descipline = fields.Float(string="Descipline")
	attendance = fields.Float(string="Attendance")

	# Leadership
	team_work = fields.Float(string="Team Work")
	team_building = fields.Float(string="Team Building")
	stratege_direction = fields.Float(string="New Stratege and Direction")
	participation_hr_act = fields.Float(string="Participation in Hr Activities")


	@api.onchange('name')
	def onchange_employee_id(self):
		if self.name:
			self.mobile_number=self.name.mobile_phone
			self.email=self.name.work_email
			self.joining_date=self.name.date_of_join
			self.designation=self.name.job_id.name
			self.department=self.name.department_id.name
			self.campus=self.name.company_id.name
			self.salary = self.name.offered_salary

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
	



class HrEmployeeInheritEvaluationButton(models.Model):
	_inherit = 'hr.employee'

	@api.multi
	def evaluation_action(self):
		return{
        'type': 'ir.actions.act_window',
        'name':'Evaluation Tracker',
        'view_mode': 'tree,form',
        'res_model': 'hr.employee.evaluation',
    	}

