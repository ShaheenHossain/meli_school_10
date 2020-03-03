import datetime

from odoo import models, fields, api, _

class DailyActionPlan(models.Model):
	_name = "daily.action"

	name = fields.Many2one("hr.employee", string="Name", required=True)
	campus = fields.Many2one('school.school', string="Campus Name", required=True)
	action_plan_date = fields.Date(string="Action Plan Date", required=True)
	s_no = fields.Integer(string="S.No")
	action_lines = fields.One2many("action.lines", 'm2o', string="Action Lines")

	@api.onchange('name')
	def NameOnchangeAction(self):
		self.campus = self.name.school_id

	@api.onchange('action_lines')
	def ActionLinesOnchangeAction(self):
		self.s_no = len(self.action_lines)+1
 

class ActionPlanLines(models.Model):
	_name = "action.lines"

	s_no = fields.Integer(string="S.No")
	name = fields.Text(string="Task Name")
	description = fields.Text(string="Action Steps Description")
	responsible = fields.Many2one("hr.department", string="Department Responsible")
	date_to_begain = fields.Date(string="Date To Begain")
	due_date = fields.Date(string="Due Date")
	comments = fields.Text(string="Comments")
	m2o = fields.Many2one("daily.action", string="Relation")
	m2o_relation = fields.Many2one("weekly.action", string="Relation")

class WeeklyActionPlan(models.Model):
	_name = "weekly.action"

	name = fields.Many2one("hr.employee", string="Name", required=True)
	campus = fields.Many2one('school.school', string="Campus Name", required=True)
	action_plan_from_date = fields.Date(string="From Date", required=True)
	action_plan_to_date = fields.Date(string="To Date", required=True)
	s_no = fields.Integer(string="S.No")
	action_lines = fields.One2many("action.lines", 'm2o_relation', string="Action Lines")

	@api.onchange('name')
	def NameOnchangeAction(self):
		self.campus = self.name.school_id

	@api.onchange('action_lines')
	def ActionLinesOnchangeAction(self):
		self.s_no = len(self.action_lines)+1


class ActionPlanTracker(models.Model):
	_name = "action.tracker"

	tracker = fields.Selection([('daily','Daily Report'),
								('weekly','Weekly Report')], required =True, string="Report Type")
	name = fields.Many2one('hr.employee', required =True, string="Employee Name")
	campus = fields.Many2one('school.school', required =True, string="Campus Name")
	from_date = fields.Date(string="From Date", required =True)
	to_date = fields.Date(string="To Date", required =True)

	@api.onchange('name')
	def NameOnchangeAction(self):
		self.campus = self.name.school_id.id

	@api.multi
	def generated_report(self):
		self.ensure_one()
		active_ids = self.env.context.get('active_ids', [])
		datas={
		'ids':active_ids,
		'model': 'action.tracker',
		'form': self.read()[0]
		}
		return self.env['report'].get_action(self,'hr_attachdoc.action_plan_tracker_report',data=datas)


class ActionPlanReportRenderhtml(models.AbstractModel):
	_name = 'report.hr_attachdoc.action_plan_tracker_report'


	@api.model
	def render_html(self, docids, data=None):
		register_ids = self.env.context.get('active_ids', [])
		from_date = data['form'].get('from_date')
		to_date = data['form'].get('to_date')
		camous = data['form'].get('campus')
		name = data['form'].get('name')
		tracker = data['form'].get('tracker')
		print tracker,"111111111111111111111"
		
		obj = self.env['daily.action'].search([])
		obj1 = self.env['weekly.action'].search([])
		count = 1
		action_data = {}
		if tracker == "daily":
			for rec in obj:
				if rec.name.id == name[0]:
					if rec.action_plan_date >= from_date and rec.action_plan_date <= to_date:
						for task in rec.action_lines:
							data = []
							data.extend([count,str(task.description),str(task.responsible.name),str(task.comments),
								str(task.name)])
							action_data[count]=data
							count = count + 1
		if tracker == "weekly":
			for rec1 in obj1:
				if rec1.name.id == name[0]:
					if rec1.action_plan_from_date >= from_date and rec1.action_plan_to_date <= to_date:
						for task in rec1.action_lines:
							data = []
							data.extend([count,str(task.description),str(task.responsible.name),str(task.comments),
								str(task.due_date),str(task.date_to_begain),str(task.name)])
							action_data[count] = data
							count = count + 1

		print action_data,"666666666666666666666666666666666"
		emp = self.env['hr.employee'].search([('id','=',name[0])])
		emp_details = []
		for employee in emp:
			emp_details.extend([str(employee.name),str(employee.school_id.name),
				str(employee.department_id.name),str(employee.job_id.name),str(from_date),str(to_date),str(tracker)])
		print emp_details,"5555555555555555555555555555555555"
							
		
		docargs = {
		'doc_model':'action.tracker',
		'data':emp_details,
		'action_data': action_data,

		}
		return self.env['report'].render('hr_attachdoc.action_plan_tracker_report', docargs)


	