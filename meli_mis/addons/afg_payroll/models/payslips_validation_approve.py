import time
from datetime import datetime, timedelta
from dateutil import relativedelta

import babel
from odoo import api, fields, models, tools, _
from odoo.exceptions import UserError, ValidationError


class VrPayslipPaymentValidation(models.Model):
	_name = "hr.afg.payroll.validation"


	name = fields.Char(string="Payment Details")
	requested_date = fields.Date(string="Requested Date")
	start_date = fields.Date(string="Start Date")
	end_date = fields.Date(string="End Date")
	document = fields.One2many('excel.report.upload', 'm2o', string="Documents")
	state = fields.Selection([('draft','HR'),
							('gm','GM/Finance'),
							('ceo','CEO'),
							('done','Done')], string="Status", default="draft")


	@api.multi
	def send_to_gm(self):
		self.write({'state':'gm'})

	@api.multi
	def send_to_ceo_action(self):
		self.write({'state':'ceo'})

	@api.multi
	def done_action(self):
		self.write({'state':'done'})


class VrpayslipXlsReportsupload(models.Model):
	_name = 'excel.report.upload'

	sequence = fields.Integer(string="S.No")
	batches = fields.Many2one('hr.afg.payroll.batches', string="Batch Name")
	document = fields.Binary(string="Document")
	m2o = fields.Many2one('hr.afg.payroll.validation')

	# @api.multi
	# def get_document(self):
	# 	print self.batches.name,"1111111111111111111111"
	# 	pass

		# new_record = self.env['employee.salary.payslip.report']
		# new_record.write({'employee_id':self.batches})
		# new_record.generated_excel_report()
		# print "111222222222222222222"
		# record = self.batches.name
		# payslips = self.env['employee.salary.payslip.report']
		# payslips.generated_excel_report('record')


