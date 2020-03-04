from datetime import datetime
from dateutil import relativedelta


from odoo import api, fields, models, _
from odoo.exceptions import UserError
from xml.dom.minidom import ReadOnlySequentialNamedNodeMap
#==================================================
# Class : BiEmployeeSalary
# Description : Employee Salary Details
#==================================================
class BiEmployeeSalary(models.Model):
	_name = "bi.employee.salary"
	_description = "Employee Salary Details"
	_order = "id desc"
	_inherit = ['ir.needaction_mixin']


	@api.model
	def _needaction_domain_get(self):
		return [('state','in',('hr_manager','finance_manager','ceo'))]
		# employees = self.env['hr.employee'].search([])
		# for employee in employees:
		# 	if self.env.user.name == employee.name:
		# 		if employee.manager == True:
		# 			return [('state', '=', 'request')]
		# 		if employee.ceo == True:
		# 			return [('state','=','hr_manager')]
		# 		if employee.finance == True:
		# 			return [('state','=','finance_manager')]


	def _get_employee_id(self):
		# assigning the related employee of the logged in user
		employee_rec = self.env['hr.employee'].search([('user_id', '=', self.env.uid)], limit=1)
		return employee_rec.id

	name = fields.Char(string="Sequence No", required=True, Index= True, default=lambda self:('New'), readonly=True)
	state = fields.Selection([
		('draft', 'Draft'),
		('hr_manager', 'Hr Approve'),
		('finance_manager','Finance Approve'),
		('ceo','CEO Approve'),
		('approve','Approved'),
		('reject', 'Rejected'),
		('closed','Closed'),
		], string='Status', readonly=True, copy=False, index=True, track_visibility='onchange', default='draft')

	employee_id = fields.Many2one('hr.employee', string = "Employee",required=True,readonly=True,states={'draft': [('readonly', False)]}, default=_get_employee_id)
	design_id = fields.Many2one('hr.job', string='Designation', required=True,readonly=True,states={'draft': [('readonly', False)]})
	amount = fields.Float(string="Request Amount",readonly=True,states={'draft': [('readonly', False)]})
	request_date = fields.Date(string="Request Date", required=True,readonly=True,states={'draft': [('readonly', False)]})
	confirm_date = fields.Date(string="Confirm Date",readonly=True)
	paid_date = fields.Date(string="Paid Date", readonly=True)
	ceo_approve_date = fields.Date(string="CEO Approval Date", readonly=True)
	confirm_manager = fields.Many2one('res.users',string="Confirm Manager",readonly=True)
	ceo_name = fields.Many2one('hr.employee',string="CEO")
	note = fields.Text(string="Employee Note",readonly=True,states={'draft': [('readonly', False)]})         
	company_id = fields.Many2one('res.company', 'Company', default=lambda self: self.env['res.company']._company_default_get('bi.employee.salary'),readonly=True,states={'draft': [('readonly', False)]})
	account_no = fields.Char("Account Number")
	ifsc_code = fields.Char("Ifsc Code")
	department_id = fields.Char("Department",readonly=True,states={'draft': [('readonly', False)]})
	manager_note = fields.Text(string="HR Remark", readonly=True, states={'hr_manager': [('readonly', False)]})
	finance_note = fields.Text(string="Finance Manager Remark",readonly=True, states={'finance_manager': [('readonly', False)]})
	ceo_note = fields.Text(string="CEO Remark", readonly=True, states={'ceo': [('readonly', False)]})
	conditions_box = fields.Boolean(string="Conditions Not Applied", readonly=True, states={'request': [('readonly', False)]},default=False)
	salary_deduction=fields.Selection([('1','1'),('2','2'),('3','3')],string='Installments',readonly=True,states={'draft': [('readonly', False)]})
	lapsed_amount = fields.Float(string="Lapsed Amount")
	
	@api.onchange('employee_id')
	def onchange_employee_id(self):
		if self.employee_id:
			self.design_id=self.employee_id.job_id
			self.account_no=self.employee_id.bank_account_no
			self.ifsc_code=self.employee_id.ifs_code
			self.department_id=self.employee_id.department_id.name
			self.company_id=self.employee_id.company_id.id
			self.request_date = fields.Date.today()


	@api.constrains('amount')
	def amount_validation(self):
		contract = self.env['hr.contract'].search([])
		for emp in contract:
			if emp.employee_id.name == self.employee_id.name:
				salary = emp.wage
				if emp.schedule_pay == "monthly":
					if not self.amount <= (salary/12)/2:
						raise UserError(_('Sorry For process Your Advance salary request must enter amount half off your salary below'))
					if self.amount == 0:
						raise UserError(_("Please Enter Advance Salary Amount"))
		return True

	@api.model
	def create(self, vals):
		if vals.get('name', _('New')) == _('New'):
			if 'company_id' in vals:
				vals['name'] = self.env['ir.sequence'].with_context(force_company=vals['company_id']).next_by_code('bi.employee.salary') or _('New')
			else:
				vals['name'] = self.env['ir.sequence'].next_by_code('bi.employee.salary') or _('New')

		result = super(BiEmployeeSalary, self).create(vals)
		return result

	
	@api.multi
	def button_request(self):
		rec=self.env['hr.contract'].search([('employee_id.name','=',self.employee_id.name)])
	
		if rec.trial_date_start < self.request_date and rec.trial_date_end > self.request_date:
			raise UserError(_('Your Trail Period Is Not Completed'))

		if self.employee_id.advance_salary_access == True:
			self.employee_id.advance_salary_access = False
			date = datetime.date(datetime.now())
			activate_date =  date + relativedelta.relativedelta(days=180)
			self.employee_id.advance_salary_date = activate_date

			

			# if self.employee_id.manager == True:
			# 	return self.write({'state': 'hr_manager'})
			return self.write({'state':'hr_manager'})
		if self.employee_id.advance_salary_access == False:
			print self.employee_id.advance_salary_date,"2222222222222"

			raise UserError('Dear Employee You are Not Eligible for Advance Salary. Please Contact Your Manager')

			
		
			

		# if self.conditions_box == True:
		# 	year_start = datetime.now().strftime('%Y-01-01')
		# 	year_end = datetime.now().strftime('%Y-%m-%d')
		# 	records = self.env['bi.employee.salary'].search([('paid_date','>=',year_start),('paid_date','<=',year_end)])
		# 	for record in records:
		# 		if record.employee_id.name == self.employee_id.name:
		# 			paid_month = record.paid_date
		# 			month = (datetime.strptime(paid_month, '%Y-%m-%d')).strftime('%m')
		# 			new_manager_date = (datetime.strptime(fields.Date.today(), '%Y-%m-%d')).strftime('%m')
		# 			if not int(new_manager_date)-int(month) >= 6 :
		# 				raise UserError(' Not Eligible for Advance Salary')
		
		# self.send_mail_template()

	@api.multi
	def send_mail_template(self):
		template = self.env.ref('bi_employee_advance.advance_salary_request_mail')
		self.env['mail.template'].browse(template.id).send_mail(self.id)


	@api.multi
	def button_reject(self):
		employee = self.env.ref('bi_employee_advance.advance_salary_reject_employee')
		manager = self.env.ref('bi_employee_advance.advance_salary_reject_manager')
		self.env['mail.template'].browse(employee.id).send_mail(self.id, force_send=True)
		self.env['mail.template'].browse(manager.id).send_mail(self.id, force_send=True)
		
		self.write({'state': 'reject'})

	@api.multi
	def button_approve(self):
		
		# if self.conditions_box == False:
		# 	year_start = datetime.now().strftime('%Y-01-01')
		# 	year_end = datetime.now().strftime('%Y-%m-%d')
		# 	records = self.env['bi.employee.salary'].search([('paid_date','>=',year_start),('paid_date','<=',year_end)])
		# 	for record in records:
		# 		if record.employee_id.name == self.employee_id.name:
		# 			paid_month = record.paid_date
		# 			month = (datetime.strptime(paid_month, '%Y-%m-%d')).strftime('%m')
		# 			new_manager_date = (datetime.strptime(fields.Date.today(), '%Y-%m-%d')).strftime('%m')
		# 			if not int(new_manager_date)-int(month) >= 6 :
		# 				raise UserError(' Not Eligible for Advance Salary')

		self.write({
			'confirm_date':fields.Date.today(),
			'confirm_manager':self.env.user.id,
			'state': 'finance_manager'})
					


	@api.multi
	def button_finance_approve(self):
		
		print "111111111111111111111"
		# employee = self.env.ref('bi_employee_advance.advance_salary_approved_employee')
		# manager = self.env.ref('bi_employee_advance.advance_salary_approved_manager')
		# finance = self.env.ref('bi_employee_advance.advance_salary_approved_finance')
		# self.env['mail.template'].browse(employee.id).send_mail(self.id, force_send=True)
		# self.env['mail.template'].browse(manager.id).send_mail(self.id, force_send=True)
		# self.env['mail.template'].browse(finance.id).send_mail(self.id, force_send=True)
		
		# Find the e-mail template
		# requester = self.env.ref('bi_employee_advance.ceo_to_requester_email')
		# hr_manager = self.env.ref('bi_employee_advance.ceo_to_hr_manager_email')
		# self.env['mail.template'].browse(requester.id).send_mail(self.id, force_send=True)
		# self.env['mail.template'].browse(hr_manager.id).send_mail(self.id, force_send=True)
		# self.env['mail.template'].browse(finance_manager.id).send_mail(self.id)
		self.write({
			'ceo_approve_date':fields.Date.today(),
			'state':'ceo'})


	@api.multi
	def button_ceo_approve(self):		
		self.write({
			'paid_date':fields.Date.today(),
			'state': 'approve'})

	@api.onchange('employee_id')
	def _onchange_employee_id(self):
		if self.employee_id:
			self.dept_id  = self.employee_id.department_id


class HrPayslip(models.Model):
	_inherit = "hr.payslip"
	@api.multi
	def compute_sheet(self):
		for payslip in self:
			advance_amount= 0.0
			advance = self.env['bi.employee.salary'].search([('employee_id','=',payslip.employee_id.id),('confirm_date','>=',payslip.date_from),('confirm_date','<=',payslip.date_to),('state','=','paid')])
			for res in advance:
				payslip_input= self.env['hr.payslip.input'].search([('payslip_id','=',payslip.id),('code','=','ADV')])
				if payslip_input:
					advance_amount+=res.amount
				payslip_input.write({
					'amount':advance_amount
					})
			# if advance and not payslip_input:
			# 	self.env['hr.payslip.input'].create({
			# 		'name':'Salary Advance',
			# 		'code':'ADV',
			# 		'amount':advance.amount,
			# 		'contract_id':payslip.contract_id.id,
			# 		'payslip_id':payslip.id
			# 		})  
		result = super(HrPayslip, self).compute_sheet()           
		return True
	# @api.multi
	# def unlink(self):
	# 	for order in self:
	# 		if order.state not in ('draft'):
	# 			raise UserError(_('You can not delete Passport bookings'))
	# 	return super(BiPassportBooking, self).unlink()



class EmployeeInheritAddAdvnaceAccess(models.Model):
	_inherit = "hr.employee"

	advance_salary_access = fields.Boolean(string="Advance Salary Access")
	advance_salary_date = fields.Date(string="Advance Salary Date")



	def advance_salary_access_activate(self):
		employees = self.env['hr.employee'].search([])
		for emp in employees:
			if emp.advance_salary_access == False:
				if emp.advance_salary_date == datetime.date(datetime.now()):
					emp.advance_salary_access = True
					emp.advance_salary_date = False






