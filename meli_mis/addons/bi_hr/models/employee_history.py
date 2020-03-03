import datetime
from datetime import datetime
from odoo.exceptions import UserError
import re

from odoo import fields, api,models,_

class EmployeeHistory(models.Model):
	_inherit = "hr.employee"

	employee_tranfer = fields.Many2many('staff.transfer', string="Employee Transfer")

	@api.multi
	def get_history(self):
		return{
	        'type': 'ir.actions.act_window',
	        'name':'History',
	        'view_mode': 'form',
	        'res_model': 'employee.history',
	        'target'   : 'inline',
		    'nodestroy': True,
	    	}

class EmployeeHistoryForm(models.TransientModel):
	_name = "employee.history"

	@api.model
	def get_history(self):
		active_id = self.env.context.get('active_id')
		employee = self.env['hr.employee'].search([('id','=',active_id)])
		records = []
		for emp in employee:
			data = self.env['staff.transfer'].search([('staff_id','=',emp.name)])
			for rec in data:
				records.append({'name':rec.staff_id,
								'date':rec.staff_date,
								'designation':rec.staff_job_id.name,
								'from_campus':rec.current_company_id.name,
								'to_campus':rec.cmp_id.name,
								'work_location':rec.staff_work_location,
								'reason':rec.staff_purpose,
								'state':dict(rec._fields['state'].selection).get(rec.state)
								})
		return records

	@api.model
	def get_compaints_history(self):
		active_id = self.env.context.get('active_id')
		employee = self.env['hr.employee'].search([('id','=',active_id)])
		records = []
		for emp in employee:
			data = self.env['hr.employee_complaint'].search([('name','=',emp.name)])
			for rec in data:
				records.append({'name':rec.name,
								'dep':rec.dep,
								'issue_date':rec.issue_date,
								'description':rec.description,
								'campus_name':rec.campus_name,
								'issue_of_dep':dict(rec._fields['issue_of_dep'].selection).get(rec.issue_of_dep),
								'state':dict(rec._fields['state'].selection).get(rec.state)
								})
		return records

	@api.model
	def GetAdvanceSalaryHistory(self):
		active_id = self.env.context.get('active_id')
		employee = self.env['hr.employee'].search([('id','=',active_id)])
		records = []
		for emp in employee:
			data = self.env['bi.employee.salary'].search([('employee_id','=',emp.name)])
			for rec in data:
				records.append({'sequence':rec.name,
								'department':rec.department_id,
								'requested_date':rec.request_date,
								'confirm_date':rec.confirm_date,
								'name':rec.employee_id,
								'designation':rec.design_id.name,
								'requested_amount':rec.amount,
								'salary_deduction':rec.salary_deduction,
								'state':dict(rec._fields['state'].selection).get(rec.state),
								})
		return records

	@api.model
	def GetMaterialHistory(self):
		active_id = self.env.context.get('active_id')
		employee = self.env['hr.employee'].search([('id','=',active_id)])
		records = []
		for emp in employee:
			data = self.env['material.request'].search([('requester','=',emp.name)])
			for rec in data:
				records.append({'name':rec.requester,
							  'school_id':rec.school_id.name,
							  'technical_team':dict(rec._fields['technical_team'].selection).get(rec.technical_team),
							  'location_id':rec.location_id.name,
							  'transfer_date':rec.transfer_date,
							  'condition':rec.condition,
							  'product':rec.material_line_ids.product_id.name,
							  'quantity':rec.material_line_ids.quantity,
							  'state':dict(rec._fields['state'].selection).get(rec.state),
							})
		return records


	employee_transfer = fields.One2many('emp.transfer', 'm2o', default=get_history, string="Employee Transfer")
	emp_complaints = fields.One2many('emp.complaints', 'm2o', default=get_compaints_history,  string="Emploee Complaints")
	emp_advance_salary = fields.One2many('emp.advnacesalary', 'm2o', default=GetAdvanceSalaryHistory, string="Advnace Salary History")
	emp_materialinfo = fields.One2many('emp.materialinfo', 'm2o', default=GetMaterialHistory, string="Emploee Material History")


	@api.multi
	def GetPrint(self):
		active_ids = self.env.context.get('active_ids', [])
		datas = {
			 'ids': active_ids,
			 'model': 'employee.history',
			 'form': self.read()[0]
			}
		return self.env['report'].get_action(self,'bi_hr.employee_history_report',data=datas)

class EmployeeHistoryFormRenderhtml(models.AbstractModel):
	_name = 'report.bi_hr.employee_history_report'


	@api.model
	def render_html(self, docids, data=None):
		register_ids = self.env.context.get('active_ids', [])
		ids = data['form'].get('id')
		obj = self.env['employee.history'].search([('id','=',ids)])
		transfer_records={}
		complaints_records={}
		advance_sl_records={}
		material_info_record={}
		for rec in obj:
			count = 1
			for transfer in rec.employee_transfer:
				transfer_data = []
				transfer_data.extend([str(transfer.name.name),str(transfer.date),str(transfer.designation),
					str(transfer.from_campus),str(transfer.to_campus),str(transfer.work_location),str(transfer.reason),str(transfer.state)])
				transfer_records[count]=transfer_data
				count = count + 1
			for complaints in rec.emp_complaints:
				complaints_data = []
				complaints_data.extend([str(complaints.name.name),str(complaints.dep),str(complaints.issue_date),
					str(complaints.campus_name),str(complaints.issue_of_dep),str(complaints.description),str(complaints.state)])
				complaints_records[count]=complaints_data
				count = count + 1
			for advance_sl in rec.emp_advance_salary:
				advance_salary = []
				advance_salary.extend([str(advance_sl.sequence),str(advance_sl.department),str(advance_sl.requested_date),str(advance_sl.confirm_date),
					str(advance_sl.name.name),str(advance_sl.designation),str(advance_sl.requested_amount),str(advance_sl.salary_deduction),str(advance_sl.state)])
				advance_sl_records[count]=advance_salary
				count = count + 1

			for material in rec.emp_materialinfo:
				material_info = []
				material_info.extend([str(material.name.name),str(material.school_id),str(material.technical_team),str(material.location_id),
					str(material.transfer_date),str(material.condition),str(material.product),str(material.quantity),str(material.state)])
				material_info_record[count]=material_info
				count = count + 1

		docargs = {
		'doc_model':'employee.history',
		'data': data,
		'transfer': transfer_records,
		'Complaints':complaints_records,
		'advance':advance_sl_records,
		'material':material_info_record,
		}
		return self.env['report'].render('bi_hr.employee_history_report', docargs)


class EmployeeTransferData(models.TransientModel):
	_name = "emp.transfer"

	name = fields.Many2one('hr.employee', string="Name")
	date = fields.Date(string="Date")
	designation = fields.Char(string="Designation")
	from_campus = fields.Char(string="From Campus")
	to_campus = fields.Char(string="To Campus")
	work_location = fields.Char(string="Work Location")
	reason = fields.Char(string="Purpose Of Change")
	state = fields.Char(string="Status")
	m2o = fields.Many2one('employee.history')

class EmployeeComplaintInfo(models.TransientModel):
	_name = "emp.complaints"

	name = fields.Many2one('hr.employee', string="Name")
	dep = fields.Char(string="Depertment")
	issue_date = fields.Char(string="Issue Date")
	description = fields.Char(string="Description")
	campus_name = fields.Char(string="Campus Name")
	issue_of_dep = fields.Char(string="Issue of Depertment")
	state = fields.Char(string="Status")
	m2o = fields.Many2one('employee.history', string="Relation")

class EmployeeAdvanceSalaryInfo(models.TransientModel):
	_name = "emp.advnacesalary"

	sequence = fields.Char(string="Sequence")
	department = fields.Char(string="Depertment")
	requested_date = fields.Char(string="Requested Date")
	confirm_date = fields.Char(string="Confirm Date")
	name = fields.Many2one('hr.employee',string="Name")
	designation = fields.Char(string="Designation")
	requested_amount = fields.Char(string="Amount")
	salary_deduction = fields.Char(string="Installments")
	state = fields.Char(string="Status")
	m2o = fields.Many2one('employee.history', string="Relation")

class EmployeeMaterialInfo(models.TransientModel):
	_name = 'emp.materialinfo'

	name = fields.Many2one('hr.employee', string="Name")
	school_id = fields.Char(string="Campus Name")
	technical_team = fields.Char(string="Technical Team")
	location_id = fields.Char(string="Location")
	transfer_date = fields.Char(string="Transfer Date")
	condition = fields.Char(string="Condition")
	product = fields.Char(string="Produt")
	quantity = fields.Char(string="Quantity")
	state = fields.Char(string="Status")
	m2o = fields.Many2one('employee.history', string="Relation")





