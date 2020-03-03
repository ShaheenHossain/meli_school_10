# -*- coding: utf-8 -*-
import time
from datetime import date, timedelta, datetime
from dateutil import relativedelta

import babel

from odoo import api, fields, models, tools, _
from odoo.exceptions import UserError, ValidationError
from odoo.tools.safe_eval import safe_eval

from odoo.addons import decimal_precision as dp

class payroll_details(models.Model):
	_name = 'hr.afg.payroll'

	
	employee_id = fields.Many2one('hr.employee',string="Employee", required=True)
	# name=fields.Char(string="Employee Name")
	mobile=fields.Char(string="Mobile")
	email =fields.Char(string="email")
	date_of_join=fields.Date(string="Date Of Join")
	campus =fields.Char(string="Campus")
	department=fields.Many2one('hr.department',string="Department")
	designation=fields.Char(string="Designation")
	start_date = fields.Date(string='Date From', required=True,
        default=time.strftime('%Y-%m-01'))
	end_date = fields.Date(string='Date To', required=True,
        default=str(datetime.now() + relativedelta.relativedelta(months=+1, day=1, days=-1))[:10])

	number =fields.Char(string="Reference", required=True, Index= True, default=lambda self:('New'), readonly=True)

	state = fields.Selection([
        ('draft', 'Draft'),
        ('verify', 'Waiting'),
        ('done', 'Done'),
        ('cancel', 'Rejected'),
    ], string='Status', index=True, readonly=True, copy=False, default='draft')
	name = fields.Char(string="Payslip Name")
	credit_note = fields.Boolean(string="Credit Note")
	payslip_run_id = fields.Many2one('hr.afg.payroll.batches',string="Payslip batches")
	# contract_id = fields.Char(string="Contract")

	@api.onchange('employee_id','start_date','end_date')
	def onchange_name(self):
		if (not self.employee_id) or (not self.start_date) or (not self.end_date):
			return

		ttyme = datetime.fromtimestamp(time.mktime(time.strptime(self.start_date, "%Y-%m-%d")))
		locale = self.env.context.get('lang') or 'en_US'
		self.name = _('Pay Stub of %s for %s') % (self.employee_id.name, tools.ustr(babel.dates.format_date(date=ttyme, format='MMMM-y', locale=locale)))
		date = datetime.strptime(self.start_date,"%Y-%m-%d")

		self.end_date = date + relativedelta.relativedelta(months=+1, day=1, days=-1)


	@api.multi
	@api.one
	def get_employee_details(self):
		if self.employee_id:
			self.write({'mobile':self.employee_id.mobile_phone,
						'email':self.employee_id.work_email,
						'date_of_join':self.employee_id.date_of_join,
						'campus':self.employee_id.school_id.name,
						'department':self.employee_id.department_id.id,
						'designation':self.employee_id.job_id.name,
						'days_of_month':0,
						'absent':0,
						'days_worked':0,
						'overtime':0,
						'base_salary':0,
						'tax':0,
						'lop':0,
						'advance_salary':0,
						'security_deposite':0,
						'bonus':0,
						'net_pay':0,
						'salary_payable':0,
						})

	@api.model
	def create(self, vals):
		if vals.get('number', _('New')) == _('New'):
			vals['number'] = self.env['ir.sequence'].next_by_code('hr.afg.payroll') or _('New')
			result = super(payroll_details, self).create(vals)
			return result


			
	@api.multi
	@api.one
	def get_days_of_month(self):
		date = datetime.strptime(self.end_date,"%Y-%m-%d")
		day = date.strftime("%d")
		self.write({'days_of_month':day})

	@api.multi
	@api.one
	def get_unpaid_leaves(self):
		rec = self.env['hr.holidays'].search([('employee_id.name','=',self.employee_id.name),('holiday_status_id.name','=','Unpaid')])
		rec1 = self.env['hr.contract'].search([('employee_id.name','=',self.employee_id.name)])
		leaves = 0
		for obj in rec:
			if self.start_date < obj.date_from and self.end_date > obj.date_to:
				leaves += obj.number_of_days_temp
		worked_days = float(self.days_of_month)-self.absent
		basesalary = rec1.wage/12
		lop_days = (basesalary/self.days_of_month)*leaves
		netpay = (basesalary-lop_days+self.bonus)
		self.write({'net_pay':netpay,
					'base_salary':basesalary,
					'absent':leaves,
					'days_worked':worked_days,
					'lop':lop_days,
					})


	@api.multi
	@api.one
	def get_all_data(self):
		self.get_employee_details()
		self.get_days_of_month()
		self.get_unpaid_leaves()
		sec_dep =0
		advance_salary =0
		value3 = 0
		salary = 0
		remaining = float(self.employee_id.offered_salary)/12 - self.employee_id.security_dp_amount
		if self.employee_id.security_dp_amount < float(self.employee_id.offered_salary)/12 and remaining > (self.base_salary/100)*5:
			sec_dep = (self.base_salary/100)*5
		# Advanced Salary
		ad_salary = self.env['bi.employee.salary'].search([('employee_id.name','=',self.employee_id.name),('state','=','approve')])
		if ad_salary.lapsed_amount != float(ad_salary.salary_deduction):
			advance_salary = float(ad_salary.amount)/float(ad_salary.salary_deduction)

		tax = self.env['state.tax'].search([])
		for taxes in tax:
			for tax_lines in taxes.state_tax_lines:
				if float(tax_lines.minimum) <= self.net_pay and float(tax_lines.maximum) >= self.net_pay:
					value = (self.net_pay - tax_lines.exemption)/100
					value2 = value*tax_lines.percentage
					value3 = value2+tax_lines.amount
		salary = self.net_pay-value3-advance_salary-sec_dep
		return self.write({'salary_payable':salary,
					'security_deposite':sec_dep,
					'advance_salary':advance_salary,
					'tax':value3
					})


	@api.multi
	def conformation_paysip(self):
		self.employee_id.security_dp_amount = self.employee_id.security_dp_amount+self.security_deposite

		ad_salary = self.env['bi.employee.salary'].search([('employee_id.name','=',self.employee_id.name),('state','=','approve')])
		if self.advance_salary != 0:
			ad_salary.lapsed_amount = ad_salary.lapsed_amount+1
		self.write({'state':'done'})
				



	# Salary Details
	days_of_month = fields.Integer(string="Days of Month")
	absent = fields.Float(string="Absent")
	days_worked = fields.Float(string="Days Worked")
	overtime = fields.Float(string="Overtime")

	base_salary = fields.Float(string="Base Salary")
	tax = fields.Float(string="Tax")
	lop = fields.Float(string="Loss of Pay")
	advance_salary = fields.Float(string="Advance Salary")
	security_deposite = fields.Float(string="Security Deposite")
	bonus = fields.Float(string="Bonus")
	net_pay = fields.Float(string="Net Pay")
	salary_payable = fields.Float(string="Salary Payable")
	other_deductions = fields.Float(string="Other Deduction")
	leaves_remaining = fields.Float(string="Leaves Balance")





class AFNStateTaxInfo(models.Model):
	_name = "state.tax"

	name = fields.Char(string="State Name")
	state_tax_lines = fields.One2many('state.tax.lines', 'm2o', string="Tax Lines")

	@api.multi
	def execute(self):
		pass

	@api.multi
	def state_tax_form(self):
		records = self.env['state.tax'].search([])
		last_record = 0
		for record in records:
			last_record = record.id
		if last_record != 0:
			return {
		        'type': 'ir.actions.act_window',
		        'res_model' : 'state.tax',
		        'view_mode' : 'form',
		        'res_id'    : last_record,
		        'target'    : 'inline',
		        'nodestroy': True,
		        }
		elif last_record == 0:
			return {
		        'type': 'ir.actions.act_window',
		        'res_model' : 'state.tax',
		        'view_mode' : 'form',
		        'target'    : 'inline',
		        }



class AFNStateTaxLines(models.Model):
	_name = 'state.tax.lines'

	minimum = fields.Integer(string="Minimum")
	maximum = fields.Integer(string="Maximum")
	percentage = fields.Integer(string="Percentage")
	amount = fields.Integer(string="Amount")
	exemption = fields.Integer(string="Exemption")
	m2o = fields.Many2one('state.tax')



class GetPayslipFromPayroll(models.Model):
	_inherit = "hr.employee"
	count=fields.Integer(string="Count",compute="_get_payslip_employee")

	@api.multi
	def get_payslips(self):

		print "1111111111111111111"
		return{
        'type': 'ir.actions.act_window',
        'name':'Pay Slips',
        'view_mode': 'tree,form',
        'res_model': 'hr.afg.payroll',
        'domain':[('employee_id.name','=',self.name)],
    	}


	@api.multi
	def _get_payslip_employee(self):
		rec=self.env['hr.afg.payroll'].search([('employee_id.name','=',self.name)])
		self.count=len(rec)


class TeacherPayroll(models.Model):
	_name = 'teacher.payroll'
	employee_id = fields.Many2one('school.teacher',string="Employee", required=True)
	# name=fields.Char(string="Employee Name")
	mobile=fields.Char(string="Mobile")
	email =fields.Char(string="email")
	date_of_join=fields.Date(string="Date Of Join")
	campus =fields.Char(string="Campus")
	department=fields.Many2one('hr.department',string="Department")
	designation=fields.Char(string="Designation")
	start_date = fields.Date(string='Date From', required=True,
        default=time.strftime('%Y-%m-01'))
	end_date = fields.Date(string='Date To', required=True,
        default=str(datetime.now() + relativedelta.relativedelta(months=+1, day=1, days=-1))[:10])

	# number =fields.Char(string="Reference", required=True, Index= True, default=lambda self:('New'), readonly=True)

	state = fields.Selection([
        ('draft', 'Draft'),
        ('verify', 'Waiting'),
        ('done', 'Done'),
        ('cancel', 'Rejected'),
    ], string='Status', index=True, readonly=True, copy=False, default='draft')
	name = fields.Char(string="Payslip Name")
	credit_note = fields.Boolean(string="Credit Note")
	payslip_run_id = fields.Many2one('hr.afg.payroll.batches',string="Payslip batches")
	# contract_id = fields.Char(string="Contract")

	@api.onchange('employee_id','start_date','end_date')
	def onchange_name(self):
		if (not self.employee_id) or (not self.start_date) or (not self.end_date):
			return

		ttyme = datetime.fromtimestamp(time.mktime(time.strptime(self.start_date, "%Y-%m-%d")))
		locale = self.env.context.get('lang') or 'en_US'
		self.name = _('Pay Stub of %s for %s') % (self.employee_id.name, tools.ustr(babel.dates.format_date(date=ttyme, format='MMMM-y', locale=locale)))
		date = datetime.strptime(self.start_date,"%Y-%m-%d")

		self.end_date = date + relativedelta.relativedelta(months=+1, day=1, days=-1)


	@api.multi
	@api.one
	def get_employee_details(self):
		if self.employee_id:
			self.write({'mobile':self.employee_id.mobile_phone,
						'email':self.employee_id.work_email,
						'date_of_join':self.employee_id.date_of_join,
						'campus':self.employee_id.school_id.name,
						'department':self.employee_id.department_id.id,
						'designation':self.employee_id.job_id.name,
						'days_of_month':0,
						'absent':0,
						'days_worked':0,
						'overtime':0,
						'base_salary':0,
						'tax':0,
						'lop':0,
						'advance_salary':0,
						'security_deposite':0,
						'bonus':0,
						'net_pay':0,
						'salary_payable':0,
						})

	# @api.model
	# def create(self, vals):
	# 	if vals.get('number', _('New')) == _('New'):
	# 		vals['number'] = self.env['ir.sequence'].next_by_code('hr.afg.payroll') or _('New')
	# 		result = super(payroll_details, self).create(vals)
	# 		return result
	def all_fridays(self):
		total_fridays = []
		year = datetime.now().strftime("%Y")    
		d = date(int(year), 1, 1)
		d += timedelta(days = 4 - d.weekday())
		while d.year == int(year):
			total_fridays.append(str(d))
			d += timedelta(days = 7)
		return total_fridays

			
	@api.multi
	@api.one
	def get_days_of_month(self):
		date = datetime.strptime(self.end_date,"%Y-%m-%d")
		day = date.strftime("%d")
		self.write({'days_of_month':day})

	@api.multi
	@api.one
	def get_unpaid_leaves(self):
		rec = self.env['hr.holidays'].search([('employee_id.name','=',self.employee_id.name),('holiday_status_id.name','=','Unpaid')])
		rec1 = self.env['hr.contract'].search([('employee_id.name','=',self.employee_id.name)])
		leaves = 0
		for obj in rec:
			if self.start_date < obj.date_from and self.end_date > obj.date_to:
				leaves += obj.number_of_days_temp
		worked_days = float(self.days_of_month)-self.absent
		basesalary = rec1.wage/12
		lop_days = (basesalary/self.days_of_month)*leaves
		netpay = (basesalary-lop_days+self.bonus)
		self.write({'net_pay':netpay,
					'base_salary':basesalary,
					'absent':leaves,
					'days_worked':worked_days,
					'lop':lop_days,
					})


	@api.multi
	@api.one
	def get_all_data(self):
		self.get_employee_details()
		self.get_days_of_month()
		self.get_unpaid_leaves()
		res=self.all_fridays()
		for friday in res:
			print friday,"33333333333333333"
		sec_dep =0
		advance_salary =0
		value3 = 0
		salary = 0
		rec=self.env['substistute.teacher'].search([])
		count=0
		for x in rec:
			if self.employee_id.id == x.s_teacher.id:
				m = datetime.now().month
				y = datetime.now().year
				ndays = (date(y, m+1, 1) - date(y, m, 1)).days
				d1 = date(y, m, 1)
				d2 = date(y, m, ndays)
				delta = d2 - d1
				dates=[(d1 + timedelta(days=i)).strftime('%Y-%m-%d') for i in range(delta.days + 1)]
				
				if x.date in dates:
					count=count+1
		self.overtime=count

		if self.overtime>0:
			r=self.days_of_month*self.per_day_hours
			z=self.base_salary/r
			t=self.overtime*z
			self.bonus=t
		remaining = float(self.employee_id.offered_salary)/12 - self.employee_id.security_dp_amount
		if self.employee_id.security_dp_amount < float(self.employee_id.offered_salary)/12 and remaining > (self.base_salary/100)*5:
			sec_dep = (self.base_salary/100)*5
		# Advanced Salary
		ad_salary = self.env['bi.employee.salary'].search([('employee_id.name','=',self.employee_id.name),('state','=','approve')])
		if ad_salary.lapsed_amount != float(ad_salary.salary_deduction):
			advance_salary = float(ad_salary.amount)/float(ad_salary.salary_deduction)

		tax = self.env['state.tax'].search([])
		for taxes in tax:
			for tax_lines in taxes.state_tax_lines:
				if float(tax_lines.minimum) <= self.net_pay and float(tax_lines.maximum) >= self.net_pay:
					value = (self.net_pay - tax_lines.exemption)/100
					value2 = value*tax_lines.percentage
					value3 = value2+tax_lines.amount
		salary = (self.net_pay-value3-advance_salary-sec_dep)+self.bonus

		return self.write({'salary_payable':salary,
					'security_deposite':sec_dep,
					'advance_salary':advance_salary,
					'tax':value3
					})


	@api.multi
	def conformation_paysip(self):
		self.employee_id.security_dp_amount = self.employee_id.security_dp_amount+self.security_deposite

		ad_salary = self.env['bi.employee.salary'].search([('employee_id.name','=',self.employee_id.name),('state','=','approve')])
		if self.advance_salary != 0:
			ad_salary.lapsed_amount = ad_salary.lapsed_amount+1
		self.write({'state':'done'})
				



	# Salary Details
	days_of_month = fields.Integer(string="Days of Month")
	absent = fields.Float(string="Absent")
	days_worked = fields.Float(string="Days Worked")
	per_day_hours=fields.Integer(string="Per Day Hours")
	overtime = fields.Float(string="Extra Classes")


	base_salary = fields.Float(string="Base Salary")
	tax = fields.Float(string="Tax")
	lop = fields.Float(string="Loss of Pay")
	advance_salary = fields.Float(string="Advance Salary")
	security_deposite = fields.Float(string="Security Deposite")
	bonus = fields.Float(string="Bonus")
	net_pay = fields.Float(string="Net Pay")
	salary_payable = fields.Float(string="Salary Payable")
	other_deductions = fields.Float(string="Other Deduction")
	leaves_remaining = fields.Float(string="Leaves Balance")

	# @api.onchange('per_day_hours')
	# def calculate_values(self):
	# 	rec=self.env['substistute.teacher'].search([])
	# 	count=0
	# 	for x in rec:
	# 		if self.employee_id.id == x.s_teacher.id:
	# 			m = datetime.now().month
	# 			y = datetime.now().year
	# 			ndays = (date(y, m+1, 1) - date(y, m, 1)).days
	# 			d1 = date(y, m, 1)
	# 			d2 = date(y, m, ndays)
	# 			delta = d2 - d1
	# 			dates=[(d1 + timedelta(days=i)).strftime('%Y-%m-%d') for i in range(delta.days + 1)]
				
	# 			if x.date in dates:
	# 				count=count+1
	# 	self.overtime=count

	# 	if self.overtime>0:
	# 		r=self.days_of_month*self.per_day_hours
	# 		z=self.base_salary/r
	# 		t=self.overtime*z
	# 		self.bonus=t
			


			


	