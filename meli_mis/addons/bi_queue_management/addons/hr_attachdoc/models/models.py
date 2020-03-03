# -*- coding: utf-8 -*-
import datetime


from odoo import models, fields, api, _

class HrRecruitmentInherit(models.Model):
	_inherit = "hr.recruitment.stage"


	interviewer_name = fields.Many2one('hr.employee', string="Interviewer Name")
	interviewer_designation = fields.Char(string="Interviewer Designation")



	@api.onchange('interviewer_name')
	def get_interviewer_designation(self):
		if self.interviewer_name.name == False:
			self.interviewer_designation = False
		else:
			self.interviewer_designation = self.interviewer_name.job_id.name


class HrEmployeeInheritedSearch(models.Model):
	_inherit = "hr.employee"

	ceo = fields.Boolean(string="Is a CEO")
	finance = fields.Boolean(string="Is a Finance")
	count=fields.Integer(string="Count",compute="_get_employee_daily_reports")



	@api.multi
	def hr_daily_report_action(self):

		return{
        'type': 'ir.actions.act_window',
        'name':'Daily Report',
        'view_mode': 'tree,form',
        'groups':'hr.group_hr_user,hr.group_hr_manager,base.group_user',
        'res_model': 'hr.dailyreport',
        'domain':[('name','=',self.name)],
    	}



	@api.multi
	def _get_employee_daily_reports(self):
		rec=self.env['hr.dailyreport'].search([('name','=',self.name)])
		self.count=len(rec)

class HrDailyWorkReport(models.Model):
	_name = "hr.dailyreport"


	@api.model
	def _default_employee_name(self):
		return self.env.user.name
		# active_ids = self.env.context.get('active_ids')		
		# employees = self.env['hr.employee'].search([])
		# for employee in employees:
		# 	if active_ids[0] == employee.id:
		# 		return employee.name
				




	name =fields.Char(string="Employee Name", default=_default_employee_name)
	manager_name = fields.Char(string="Manager Name")
	month = fields.Char(string="Month Name")
	work_date = fields.Datetime(string="Work Date")
	report_o2m =fields.One2many('hr.dailytask','report_m2o', string="Testing")

	upcoming_work = fields.Text(string="Upcoming Work Report")


	@api.onchange('name')
	def name_onchange(self):
		employee = self.env['hr.employee'].search([('name','=',self.name)])
		self.manager_name = employee.line_manager_id.name
		mydate = datetime.datetime.now()
		self.month = mydate.strftime("%B")
		self.work_date = datetime.datetime.now()




class HrDailyReportTaskFiled(models.Model):
	_name = "hr.dailytask"


	name = fields.Char(string="Tasks")
	description = fields.Char(string="Description of Work Performed")
	planned_date = fields.Date(string="Planned Finish Date")
 	estimated_date = fields.Date(string="Estimated Complete Date")
	current_status = fields.Char(string="Current Status")
	report_m2o = fields.Many2one('hr.dailyreport')


