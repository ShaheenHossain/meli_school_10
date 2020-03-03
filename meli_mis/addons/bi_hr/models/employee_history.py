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
		# data = self.env['staff.transfer'].search([('staff_id','=',self.name)])
		# print data,"222222222222222222222222222"
		# records = []
		# for rec in data:
		# 	print rec.id,"1111111111111111111111111111"
		# 	records.append({'name':rec.staff_id,
		# 					'date':rec.staff_date,
		# 					'designation':rec.staff_job_id,
		# 					'from_campus':rec.current_company_id,
		# 					'to_campus':rec.cmp_id,
		# 					'work_location':rec.staff_work_location,
		# 					'reason':rec.staff_purpose})

		# self.employee_tranfer = records


		# print records,"33333333333333333333333"



		return{
	        'type': 'ir.actions.act_window',
	        'name':'History',
	        'view_mode': 'form',
	        'res_model': 'employee.history',
	      #   'context':{
	      #          'default_employee_transfer' : records,
	    		# }
	    	}



	@api.multi
	def ItTicketing_Request(self):
		return{
	        'type': 'ir.actions.act_window',
	        'name':'IT Request',
	        'view_mode': 'tree,form',
	        'res_model': 'it.request',
	        'domain':[('requester.id','=',self.id)],
	        'context':{'create':False,
	        		   'delete':False,
	        		   'edit':False}
	        }


class EmployeeHistoryForm(models.TransientModel):
	_name = "employee.history"

	@api.model
	def get_history(self):
		active_id = self.env.context.get('active_id')
		print active_id,"1111111111111111111111111"

		employee = self.env['hr.employee'].search([('id','=',active_id)])
		print "2222222222222222222222222222"
		records = []
		for emp in employee:
			data = self.env['staff.transfer'].search([(('staff_id','=',emp.name))])
			print data,"33333333333333333333333333"
			for rec in data:
				print rec.id,"1111111111111111111111111111"
				records.append({'name':rec.staff_id,
								'date':rec.staff_date,
								'designation':rec.staff_job_id.name,
								'from_campus':rec.current_company_id.name,
								'to_campus':rec.cmp_id.name,
								'work_location':rec.staff_work_location,
								'reason':rec.staff_purpose})
		return records

	employee_transfer = fields.One2many('emp.transfer', 'm2o', default=get_history, string="Employee Transfer")

class EmployeeTransferData(models.TransientModel):
		_name = "emp.transfer"

		name = fields.Many2one('hr.employee', string="Name")
		date = fields.Date(string="Date")
		designation = fields.Char(string="Designation")
		from_campus = fields.Char(string="From Campus")
		to_campus = fields.Char(string="To Campus")
		work_location = fields.Char(string="Work Location")
		reason = fields.Char(string="Purpose Of Change")
		m2o = fields.Many2one('employee.history')




