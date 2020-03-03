from odoo.exceptions import UserError
from datetime import datetime


from odoo import models, fields, api,_


# For Maintenance of Campus

class MaintenanceofCampus(models.Model):
	_name = "audit.maintenance"

	
	
	name=fields.Many2one('school.school',string="Campus")
	date_of_audit=fields.Date('Date Of Audit')
	total=fields.Integer('Total',compute='_calculate_percentage_of_campus_audting')
	percentage=fields.Float('Percentage',compute='_calculate_percentage_of_campus_audting')
	month_of_auditing=fields.Char('Month Of Auditing',compute='_calculate_percentage_of_campus_audting')
	maintenance_description_id=fields.One2many('maintanance.description','main_des')
	maintance_id=fields.One2many('audit.maintenancelines','maintanence_lines')
	s_no=fields.Char('Serial No')

	@api.onchange('maintenance_description_id')
	def _get_s_no(self):
		self.s_no = len(self.maintenance_description_id)+1

	@api.onchange('name')
	def get_maintenance_questions(self):
		rec=self.env['audit.configuration'].search([])
		questions=[]
		for x in rec:
			question_type = dict(x._fields['name'].selection).get(x.name)
			if question_type=='Maintenance of Campus':
				questions.append(({'maintenance':x.question}))
		self.maintance_id=questions

	@api.one
	@api.model
	def _calculate_percentage_of_campus_audting(self):
		date=self.date_of_audit
		d = datetime.strptime(date, '%Y-%m-%d')
		self.month_of_auditing=str(d.strftime("%B"))
		values=0
		count=0
		for x in self.maintance_id:
			if x.excellent==True:
				count=count+4
				values=values+1
			if x.good==True:
				count=count+3
				values=values+1
			if x.poor==True:
				count=count+2
				values=values+1
			if x.unacceptable==True:
				count=count+1
				values=values+1
		self.total=count
		self.percentage=(count*100)/(values*4)

	
class MaintenanceofCampusLines(models.Model):
	_name='audit.maintenancelines'


	maintenance=fields.Char(string="Audit Questions",readonly=True)
	excellent=fields.Boolean(string="Excellent")
	good=fields.Boolean(string="Good")
	poor=fields.Boolean(string="Poor")
	unacceptable=fields.Boolean(string="Unacceptable")
	reason =fields.Char(string="Reason")
	maintanence_lines=fields.Many2one('audit.maintenance')


	@api.onchange('excellent')
	def onchanging_excellent(self):
		if self.excellent!=0:
			self.good=0
			self.poor=0
			self.unacceptable=0

	@api.onchange('poor')
	def onchanging_poor(self):
		if self.poor!=0:
			self.good=0
			self.excellent=0
			self.unacceptable=0

	@api.onchange('good')
	def onchanging_good(self):
		if self.good!=0:
			self.poor=0
			self.excellent=0
			self.unacceptable=0

	@api.onchange('unacceptable')
	def onchanging_unacceptable(self):
		if self.unacceptable!=0:
			self.poor=0
			self.excellent=0
			self.good=0



	@api.onchange('unacceptable')
	def validate_unacceptable(self):
		if self.unacceptable==True:
			raise UserError('Please Write Unacceptable Reason')


class maintainanceDescription(models.Model):
	_name = 'maintanance.description'

	s_no =fields.Integer('Serial No.',)
	des=fields.Text('Findings')
	state=fields.Selection([('confirm','Confirm'),('hold','Hold'),('close','Closed')],string="Status",default='confirm',readonly=True)
	planned_date=fields.Date('Issue Raised Date',default=fields.Date.context_today,readonly=True)
	close_date=fields.Date('Closed Date',readonly=True)
	main_des=fields.Many2one('audit.maintenance')
	reason=fields.Text('Holding Reason')


	

	@api.multi
	def holding_process(self):
		self.state='hold'

	@api.multi
	def close_problem(self):
		self.close_date=datetime.now()
		self.write({'state':'close'})

	@api.constrains('state')
	def validate_reason(self):
		if self.state=='hold':
			if self.reason==False:
				raise UserError(_('Please  Write The Holding Reason'))
			


# For Assistant Academy Manager

class AssistantAcademyManager(models.Model):
	_name='audit.academy'


	name=fields.Many2one('school.school',string="Campus")
	date_of_audit=fields.Date('Date Of Audit')
	total=fields.Integer('Total',compute='_calculate_academy_audting')
	percentage=fields.Float('Percentage',compute='_calculate_academy_audting')
	month_of_auditing=fields.Char('Month Of Auditing',compute='_calculate_academy_audting')
	academy_id=fields.One2many('audit.academylines','academy_lines')
	academy_description_id=fields.One2many('acedamy.description','academy_des')
	s_no=fields.Char('Serial No')

	@api.onchange('academy_id')
	def _get_s_no(self):
		self.s_no = len(self.academy_id)+1
	
	


	@api.onchange('name')
	def getAssistantAcademyManager_questions(self):
		rec=self.env['audit.configuration'].search([])
		questions=[]
		for x in rec:
			question_type = dict(x._fields['name'].selection).get(x.name)
			if question_type=='Assistant Academy Manager':
				questions.append(({'academy':x.question}))
		self.academy_id=questions

	@api.one
	@api.model
	def _calculate_academy_audting(self):
		date=self.date_of_audit
		d = datetime.strptime(date, '%Y-%m-%d')
		self.month_of_auditing=str(d.strftime("%B"))
		values=0
		count=0
		for x in self.academy_id:
			if x.excellent==True:
				count=count+4
				values=values+1
			if x.good==True:
				count=count+3
				values=values+1
			if x.poor==True:
				count=count+2
				values=values+1
			if x.unacceptable==True:
				count=count+1
				values=values+1
		self.total=count
		self.percentage=(count*100)/(values*4)

	



class AssistanAcademyManagerLines(models.Model):
	_name='audit.academylines'


	academy=fields.Char(string="Audit Questions",readonly=True)
	excellent=fields.Boolean(string="Excellent")
	good=fields.Boolean(string="Good")
	poor=fields.Boolean(string="Poor")
	unacceptable=fields.Boolean(string="Unacceptable")
	reason =fields.Char(string="Reason")
	academy_lines=fields.Many2one('audit.academy')

	@api.onchange('excellent')
	def onchanging_excellent(self):
		if self.excellent!=0:
			self.good=0
			self.poor=0
			self.unacceptable=0

	@api.onchange('poor')
	def onchanging_poor(self):
		if self.poor!=0:
			self.good=0
			self.excellent=0
			self.unacceptable=0

	@api.onchange('good')
	def onchanging_good(self):
		if self.good!=0:
			self.poor=0
			self.excellent=0
			self.unacceptable=0

	@api.onchange('unacceptable')
	def onchanging_unacceptable(self):
		if self.unacceptable!=0:
			self.poor=0
			self.excellent=0
			self.good=0


class AcedamyDescription(models.Model):
	_name = 'acedamy.description'

	s_no =fields.Integer('Serial No.',)
	des=fields.Text('Findings')
	state=fields.Selection([('confirm','Confirm'),('hold','Hold'),('close','Closed')],string="Status",default='confirm',readonly=True)
	planned_date=fields.Date('Issue Raised Date',default=fields.Date.context_today,readonly=True)
	close_date=fields.Date('Closed Date',readonly=True)
	academy_des=fields.Many2one('audit.academy')
	reason=fields.Text('Holding Reason')

	@api.multi
	def holding_process(self):
		self.state='hold'

	@api.multi
	def close_problem(self):
		self.close_date=datetime.now()
		self.write({'state':'close'})

	@api.constrains('state')
	def validate_reason(self):
		if self.state=='hold':
			if self.reason==False:
				raise UserError(_('Please  Write The Holding Reason'))


# For Counseling Process

class CounselingProcess(models.Model):
	_name = 'audit.counsiling'

	

	name=fields.Many2one('school.school',string="Campus")
	date_of_audit=fields.Date('Date Of Audit')
	total=fields.Integer('Total',compute='_calculate_counsiling_audting')
	percentage=fields.Float('Percentage',compute='_calculate_counsiling_audting')
	academy_id=fields.One2many('audit.counsilinglines','counsiling_lines',compute="_get_CounselingProcess_questions")
	month_of_auditing=fields.Char('Month Of Auditing',compute='_calculate_counsiling_audting')
	counsiling_description_id=fields.One2many('counsiling.description','counsiling_des')
	s_no=fields.Char('Serial No')

	@api.onchange('academy_id')
	def _get_s_no(self):
		self.s_no = len(self.academy_id)+1

	@api.onchange('name')
	def _get_CounselingProcess_questions(self):
		rec=self.env['audit.configuration'].search([])

		questions=[]
		for x in rec:
			question_type = dict(x._fields['name'].selection).get(x.name)
			if question_type=="Counseling Process":
				questions.append(({'counsiling':x.question}))
		self.academy_id=questions

	@api.one
	@api.model
	def _calculate_counsiling_audting(self):
		date=self.date_of_audit
		d = datetime.strptime(date, '%Y-%m-%d')
		self.month_of_auditing=str(d.strftime("%B"))
		values=0
		count=0
		for x in self.academy_id:
			if x.excellent==True:
				count=count+4
				values=values+1
			if x.good==True:
				count=count+3
				values=values+1
			if x.poor==True:
				count=count+2
				values=values+1
			if x.unacceptable==True:
				count=count+1
				values=values+1
		self.total=count
		self.percentage=(count*100)/(values*4)



class CounselingProcessLines(models.Model):
	_name='audit.counsilinglines'


	counsiling=fields.Char(string="Audit Questions",readonly=True)
	excellent=fields.Integer(string="Excellent")
	good=fields.Integer(string="Good")
	poor=fields.Integer(string="Poor")
	unacceptable=fields.Integer(string="Unacceptable")
	reason =fields.Char(string="Reason")
	counsiling_lines=fields.Many2one('audit.counsiling')
	@api.onchange('excellent')
	def onchanging_excellent(self):
		if self.excellent!=0:
			self.good=0
			self.poor=0
			self.unacceptable=0

	@api.onchange('poor')
	def onchanging_poor(self):
		if self.poor!=0:
			self.good=0
			self.excellent=0
			self.unacceptable=0

	@api.onchange('good')
	def onchanging_good(self):
		if self.good!=0:
			self.poor=0
			self.excellent=0
			self.unacceptable=0

	@api.onchange('unacceptable')
	def onchanging_unacceptable(self):
		if self.unacceptable!=0:
			self.poor=0
			self.excellent=0
			self.good=0



	@api.onchange('unacceptable')
	def validate_unacceptable(self):
		if self.unacceptable==True:
			raise UserError('Please Write Unacceptable Reason')

class CounsilingDescription(models.Model):
	_name = 'counsiling.description'

	s_no =fields.Integer('Serial No.',)
	des=fields.Text('Findings')
	state=fields.Selection([('confirm','Confirm'),('hold','Hold'),('close','Closed')],string="Status",default='confirm',readonly=True)
	planned_date=fields.Date('Issue Raised Date',default=fields.Date.context_today,readonly=True)
	close_date=fields.Date('Closed Date',readonly=True)
	counsiling_des=fields.Many2one('audit.counsiling')
	reason=fields.Text('Holding Reason')

	@api.multi
	def holding_process(self):
		self.state='hold'

	@api.multi
	def close_problem(self):
		self.close_date=datetime.now()
		self.write({'state':'close'})

	@api.constrains('state')
	def validate_reason(self):
		if self.state=='hold':
			if self.reason==False:
				raise UserError(_('Please  Write The Holding Reason'))


# For Examination Department

class ExaminationDepartment(models.Model):
	_name = "audit.examination"

	name=fields.Many2one('school.school',string="Campus")
	date_of_audit=fields.Date('Date Of Audit')
	total=fields.Integer('Total',compute='_calculate_examination_audting')
	percentage=fields.Float('Percentage',compute='_calculate_examination_audting')
	academy_id=fields.One2many('audit.examinationlines','examination_lines',compute='_get_ExaminationDepartment_questions')
	month_of_auditing=fields.Char('Month Of Auditing',compute='_calculate_examination_audting')
	examination_description_id=fields.One2many('examination.description','examination_des')
	s_no=fields.Char('Serial No')

	@api.onchange('academy_id')
	def _get_s_no(self):
		self.s_no = len(self.academy_id)+1	

	@api.onchange('name')
	def _get_ExaminationDepartment_questions(self):
		rec=self.env['audit.configuration'].search([])
		questions=[]
		for x in rec:
			question_type = dict(x._fields['name'].selection).get(x.name)
			if question_type=='Examination Department':
				questions.append(({'examination':x.question}))
		self.academy_id=questions

	
					
	@api.one
	@api.model
	def _calculate_examination_audting(self):
		date=self.date_of_audit
		d = datetime.strptime(date, '%Y-%m-%d')
		self.month_of_auditing=str(d.strftime("%B"))
		values=0
		count=0
		for x in self.academy_id:
			if x.excellent==True:
				count=count+4
				values=values+1
			if x.good==True:
				count=count+3
				values=values+1
			if x.poor==True:
				count=count+2
				values=values+1
			if x.unacceptable==True:
				count=count+1
				values=values+1
		self.total=count
		self.percentage=(count*100)/(values*4)
		

class ExaminationDepartmentLines(models.Model):
	_name='audit.examinationlines'


	examination=fields.Char(string="Audit Questions",readonly=True)
	excellent=fields.Integer(string="Excellent")
	good=fields.Integer(string="Good")
	poor=fields.Integer(string="Poor")
	unacceptable=fields.Integer(string="Unacceptable")
	reason =fields.Char(string="Reason")
	examination_lines=fields.Many2one('audit.examination')
	@api.onchange('excellent')
	def onchanging_excellent(self):
		if self.excellent!=0:
			self.good=0
			self.poor=0
			self.unacceptable=0

	@api.onchange('poor')
	def onchanging_poor(self):
		if self.poor!=0:
			self.good=0
			self.excellent=0
			self.unacceptable=0

	@api.onchange('good')
	def onchanging_good(self):
		if self.good!=0:
			self.poor=0
			self.excellent=0
			self.unacceptable=0

	@api.onchange('unacceptable')
	def onchanging_unacceptable(self):
		if self.unacceptable!=0:
			self.poor=0
			self.excellent=0
			self.good=0


	@api.onchange('unacceptable')
	def validate_unacceptable(self):
		if self.unacceptable==True:
			raise UserError('Please Write Unacceptable Reason')


class ExaminationDescription(models.Model):
	_name = 'examination.description'

	s_no =fields.Integer('Serial No.',)
	des=fields.Text('Findings')
	state=fields.Selection([('confirm','Confirm'),('hold','Hold'),('close','Closed')],string="Status",default='confirm',readonly=True)
	planned_date=fields.Date('Issue Raised Date',default=fields.Date.context_today,readonly=True)
	close_date=fields.Date('Closed Date',readonly=True)
	examination_des=fields.Many2one('audit.examination')
	reason=fields.Text('Holding Reason')

	@api.multi
	def holding_process(self):
		self.state='hold'

	@api.multi
	def close_problem(self):
		self.close_date=datetime.now()
		self.write({'state':'close'})

	@api.constrains('state')
	def validate_reason(self):
		if self.state=='hold':
			if self.reason==False:
				raise UserError(_('Please  Write The Holding Reason'))


class FinanceExecutive(models.Model):
	_name = 'audit.finance'

	

	name=fields.Many2one('school.school',string="Campus")
	date_of_audit=fields.Date('Date Of Audit')
	total=fields.Integer('Total',compute='_calculate_finance_audting')
	percentage=fields.Float('Percentage',compute='_calculate_finance_audting')
	month_of_auditing=fields.Char('Month Of Auditing',compute='_calculate_finance_audting')
	academy_id=fields.One2many('audit.financelines','finance_lines')
	finance_description_id=fields.One2many('finance.description','finance_lines1')
	s_no=fields.Char('Serial No')

	@api.onchange('academy_id')
	def _get_s_no(self):
		self.s_no = len(self.academy_id)+1


	@api.onchange('name')
	def _get_FinanceExecutive_questions(self):
		rec=self.env['audit.configuration'].search([])
		questions=[]
		for x in rec:
			question_type = dict(x._fields['name'].selection).get(x.name)
			if question_type=='Finance Executive':
				questions.append(({'finance':x.question}))
		self.academy_id=questions

	@api.one
	@api.model
	def _calculate_finance_audting(self):
		date=self.date_of_audit
		d = datetime.strptime(date, '%Y-%m-%d')
		self.month_of_auditing=str(d.strftime("%B"))
		values=0
		count=0
		for x in self.academy_id:
			if x.excellent==True:
				count=count+4
				values=values+1
			if x.good==True:
				count=count+3
				values=values+1
			if x.poor==True:
				count=count+2
				values=values+1
			if x.unacceptable==True:
				count=count+1
				values=values+1
		self.total=count
		self.percentage=(count*100)/(values*4)
		

class FinanceExecutiveLines(models.Model):
	_name='audit.financelines'


	finance=fields.Char(string="Audit Questions",readonly=True)
	excellent=fields.Integer(string="Excellent")
	good=fields.Integer(string="Good")
	poor=fields.Integer(string="Poor")
	unacceptable=fields.Integer(string="Unacceptable")
	reason =fields.Char(string="Reason")
	finance_lines=fields.Many2one('audit.finance')
	@api.onchange('excellent')
	def onchanging_excellent(self):
		if self.excellent!=0:
			self.good=0
			self.poor=0
			self.unacceptable=0

	@api.onchange('poor')
	def onchanging_poor(self):
		if self.poor!=0:
			self.good=0
			self.excellent=0
			self.unacceptable=0

	@api.onchange('good')
	def onchanging_good(self):
		if self.good!=0:
			self.poor=0
			self.excellent=0
			self.unacceptable=0

	@api.onchange('unacceptable')
	def onchanging_unacceptable(self):
		if self.unacceptable!=0:
			self.poor=0
			self.excellent=0
			self.good=0




	

	@api.onchange('unacceptable')
	def validate_unacceptable(self):
		if self.unacceptable==True:
			raise UserError('Please Write Unacceptable Reason')


class FinanceDescription(models.Model):
	_name = 'finance.description'

	s_no =fields.Integer('Serial No.',)
	des=fields.Text('Findings')
	state=fields.Selection([('confirm','Confirm'),('hold','Hold'),('close','Closed')],string="Status",default='confirm',readonly=True)
	planned_date=fields.Date('Issue Raised Date',default=fields.Date.context_today,readonly=True)
	close_date=fields.Date('Closed Date',readonly=True)
	finance_lines1=fields.Many2one('audit.finance')
	reason=fields.Text('Holding Reason')

	@api.multi
	def holding_process(self):
		self.state='hold'

	@api.multi
	def close_problem(self):
		self.close_date=datetime.now()
		self.write({'state':'close'})

	@api.constrains('state')
	def validate_reason(self):
		if self.state=='hold':
			if self.reason==False:
				raise UserError(_('Please  Write The Holding Reason'))



# For Security Guard
class SecurityGuard(models.Model):
	_name = 'audit.security'

	


	name=fields.Many2one('school.school',string="Campus")
	date_of_audit=fields.Date('Date Of Audit')
	total=fields.Integer('Total',compute='_calculate_security_audting')
	percentage=fields.Float('Percentage',compute='_calculate_security_audting')
	month_of_auditing=fields.Char('Month Of Auditing',compute='_calculate_security_audting')
	academy_id=fields.One2many('audit.securitylines','security_lines')
	security_description_id=fields.One2many('security.description','security_des')
	s_no=fields.Char('Serial No')

	@api.onchange('academy_id')
	def _get_s_no(self):
		self.s_no = len(self.academy_id)+1
	@api.onchange('name')
	def _get_SecurityExecutive_questions(self):
		rec=self.env['audit.configuration'].search([])
		
		questions=[]
		for x in rec:
			question_type = dict(x._fields['name'].selection).get(x.name)
			if question_type=='Security Guard':
				questions.append(({'security':x.question}))
		print questions
		self.academy_id=questions

	@api.one
	@api.model
	def _calculate_finance_audting(self):
		date=self.date_of_audit
		d = datetime.strptime(date, '%Y-%m-%d')
		self.month_of_auditing=str(d.strftime("%B"))
		values=0
		count=0
		for x in self.academy_id:
			if x.excellent==True:
				count=count+4
				values=values+1
			if x.good==True:
				count=count+3
				values=values+1
			if x.poor==True:
				count=count+2
				values=values+1
			if x.unacceptable==True:
				count=count+1
				values=values+1
		self.total=count
		self.percentage=(count*100)/(values*4)

	

class SecurityGuardLines(models.Model):
	_name='audit.securitylines'

	security=fields.Char(string="Audit Questions",readonly=True)
	excellent=fields.Integer(string="Excellent")
	good=fields.Integer(string="Good")
	poor=fields.Integer(string="Poor")
	unacceptable=fields.Integer(string="Unacceptable")
	reason =fields.Char(string="Reason")
	security_lines=fields.Many2one('audit.security')
	@api.onchange('excellent')
	def onchanging_excellent(self):
		if self.excellent!=0:
			self.good=0
			self.poor=0
			self.unacceptable=0

	@api.onchange('poor')
	def onchanging_poor(self):
		if self.poor!=0:
			self.good=0
			self.excellent=0
			self.unacceptable=0

	@api.onchange('good')
	def onchanging_good(self):
		if self.good!=0:
			self.poor=0
			self.excellent=0
			self.unacceptable=0

	@api.onchange('unacceptable')
	def onchanging_unacceptable(self):
		if self.unacceptable!=0:
			self.poor=0
			self.excellent=0
			self.good=0

	@api.onchange('unacceptable')
	def validate_unacceptable(self):
		if self.unacceptable==True:
			raise UserError('Please Write Unacceptable Reason')

class SecurityDescription(models.Model):
	_name = 'security.description'

	s_no =fields.Integer('Serial No.',)
	des=fields.Text('Findings')
	state=fields.Selection([('confirm','Confirm'),('hold','Hold'),('close','Closed')],string="Status",default='confirm',readonly=True)
	planned_date=fields.Date('Issue Raised Date',default=fields.Date.context_today,readonly=True)
	close_date=fields.Date('Closed Date',readonly=True)
	security_des=fields.Many2one('audit.security')
	reason=fields.Text('Holding Reason')

	@api.multi
	def holding_process(self):
		self.state='hold'

	@api.multi
	def close_problem(self):
		self.close_date=datetime.now()
		self.write({'state':'close'})

	@api.constrains('state')
	def validate_reason(self):
		if self.state=='hold':
			if self.reason==False:
				raise UserError(_('Please  Write The Holding Reason'))


# FOr Attendance Process

class AttendanceProcess(models.Model):
	_name ="audit.audit.attendance"

	name=fields.Many2one('school.school',string="Campus")
	date_of_audit=fields.Date('Date Of Audit')
	total=fields.Integer('Total',compute='_calculate_attendance_audting')
	percentage=fields.Float('Percentage',compute='_calculate_attendance_audting')
	month_of_auditing=fields.Char('Month Of Auditing',compute='_calculate_attendance_audting')
	academy_id=fields.One2many('audit.audit.attendancelines','attendance_lines')
	attendance_description_id=fields.One2many('attendance.description','attendance_des')
	s_no=fields.Char('Serial No')

	@api.onchange('academy_id')
	def _get_s_no(self):
		self.s_no = len(self.academy_id)+1

	@api.onchange('name')
	def _get_AttendanceProcess_questions(self):
		rec=self.env['audit.configuration'].search([])
		questions=[]
		for x in rec:
			question_type = dict(x._fields['name'].selection).get(x.name)
			if question_type=='Attendance Process':
				questions.append(({'attendance':x.question}))
		print questions
		self.academy_id=questions

	@api.one
	@api.model
	def _calculate_finance_audting(self):
		date=self.date_of_audit
		d = datetime.strptime(date, '%Y-%m-%d')
		self.month_of_auditing=str(d.strftime("%B"))
		values=0
		count=0
		for x in self.academy_id:
			if x.excellent==True:
				count=count+4
				values=values+1
			if x.good==True:
				count=count+3
				values=values+1
			if x.poor==True:
				count=count+2
				values=values+1
			if x.unacceptable==True:
				count=count+1
				values=values+1
		self.total=count
		self.percentage=(count*100)/(values*4)

class AttendanceProcessLines(models.Model):
	_name='audit.audit.attendancelines'


	attendance=fields.Char(string="Audit Questions",readonly=True)
	excellent=fields.Integer(string="Excellent")
	good=fields.Integer(string="Good")
	poor=fields.Integer(string="Poor")
	unacceptable=fields.Integer(string="Unacceptable")
	reason =fields.Char(string="Reason")
	attendance_lines=fields.Many2one('audit.audit.attendance')

	@api.onchange('excellent')
	def onchanging_excellent(self):
		if self.excellent!=0:
			self.good=0
			self.poor=0
			self.unacceptable=0

	@api.onchange('poor')
	def onchanging_poor(self):
		if self.poor!=0:
			self.good=0
			self.excellent=0
			self.unacceptable=0

	@api.onchange('good')
	def onchanging_good(self):
		if self.good!=0:
			self.poor=0
			self.excellent=0
			self.unacceptable=0

	@api.onchange('unacceptable')
	def onchanging_unacceptable(self):
		if self.unacceptable!=0:
			self.poor=0
			self.excellent=0
			self.good=0


	@api.onchange('unacceptable')
	def validate_unacceptable(self):
		if self.unacceptable==True:
			raise UserError('Please Write Unacceptable Reason')

class AttendanceDescription(models.Model):
	_name = 'attendance.description'

	s_no =fields.Integer('Serial No.',)
	des=fields.Text('Findings')
	state=fields.Selection([('confirm','Confirm'),('hold','Hold'),('close','Closed')],string="Status",default='confirm',readonly=True)
	planned_date=fields.Date('Issue Raised Date',default=fields.Date.context_today,readonly=True)
	close_date=fields.Date('Closed Date',readonly=True)
	attendance_des=fields.Many2one('audit.audit.attendance')
	reason=fields.Text('Holding Reason')

	@api.multi
	def holding_process(self):
		self.state='hold'

	@api.multi
	def close_problem(self):
		self.close_date=datetime.now()
		self.write({'state':'close'})

	@api.constrains('state')
	def validate_reason(self):
		if self.state=='hold':
			if self.reason==False:
				raise UserError(_('Please  Write The Holding Reason'))




class WholeAuditingReport(models.Model):
	_name='audit.audit'
	
	
	@api.model
	def _get_auditing_questions(self):
		auditing_values=['Maintenance of Campus',
						'Assistant Academy Manager',
						'Counseling Process',
						'Examination Department',
						'Finance Executive',
						'Security Guard',
						'Attendance Process',
						]
		values=[]
		for x in auditing_values:
			values.append(({'description':x}))
		return values




	name=fields.Many2one('school.school',string='Campus')
	date=fields.Selection([(1, 'January'), 
						   (2, 'February'),
						   (3, 'March'), 
						   (4, 'April'), 
						   (5, 'May'),
						   (6, 'June'), 
						   (7, 'July'), 
						   (8, 'August'), 
						   (9, 'September'), 
						   (10, 'October'), 
						   (11, 'November'), 
						   (12, 'December')],string="Select Auditing Month")

	total=fields.Integer('Total Auditing Marks')
	percentage=fields.Float('Percentage')
	whole_audit_id=fields.One2many('audit.auditlines','audit_lines',default=_get_auditing_questions)

	# @api.model
	# def _calculate_attendance_audting11(self):
	# 	print "33333333333333333333333333"
	# 	# count=0
	# 	# for x in self.whole_audit_id:
	# 	# 	count=count+x.marks
	# 	# self.total=count


	@api.onchange('campus','date')
	def getting_all_data(self):
		days = dict(self._fields['date'].selection).get(self.date)
		rec=self.env['audit.maintenance'].search([])
		academy_rec=self.env['audit.academy'].search([])
		counsiling_rec=self.env['audit.counsiling'].search([])
		examination_rec=self.env['audit.examination'].search([])
		finance_rec=self.env['audit.finance'].search([])
		security_rec=self.env['audit.security'].search([])
		attendance_rec=self.env['audit.audit.attendance'].search([])
		for x in self.whole_audit_id:
			x.marks=False
			x.percentage=False

			if x.description=='Maintenance of Campus':
				for y in rec:
					if self.name.name==y.name.name and days==y.month_of_auditing:
						x.marks=y.total
						x.percentage=y.percentage
						
			if x.description=='Assistant Academy Manager':
				for y in academy_rec:
					if self.name.name==y.name.name and self.date==y.month_of_auditing:
						x.marks=y.total
						x.percentage=y.percentage
						
			if x.description=='Counseling Process':
				for y in counsiling_rec:
					if self.name.name==y.name.name and self.date==y.month_of_auditing:
						x.marks=y.total
						x.percentage=y.percentage
						
			if x.description=='Examination Department':
				for y in examination_rec:
					if self.name.name==y.name.name and self.date==y.month_of_auditing:
						x.marks=y.total
						x.percentage=y.percentage
						
			if x.description=='Finance Executive':
				for y in finance_rec:
					if self.name.name==y.name.name and self.date==y.month_of_auditing:
						x.marks=y.total
						x.percentage=y.percentage
						
			if x.description=='Security Guard':
				for y in security_rec:
					if self.name.name==y.name.name and self.date==y.month_of_auditing:
						x.marks=y.total
						x.percentage=y.percentage
						
			if x.description=='Attendance Process':
				for y in attendance_rec:
					if self.name.name==y.name.name and self.date==y.month_of_auditing:
						x.marks=y.total
						x.percentage=y.percentage
						
		count=0
		for x in self.whole_audit_id:
			count=count+x.marks
		percentage=(count*100)/500
		self.total=count
		self.percentage=percentage


class WholeAuditingReportLines(models.Model):
	_name ='audit.auditlines'

	description=fields.Char('Type Of Audit',)
	marks=fields.Integer('Total Marks')
	percentage=fields.Integer('Percentage')
	status=fields.Char(string='Status')
	closing_date=fields.Date('Closing Date')
	audit_lines=fields.Many2one('audit.audit')



class AuditingConfigurarion(models.Model):
	_name = 'audit.configuration'

	name=fields.Selection([('1','Maintenance of Campus'),
							('2','Assistant Academy Manager'),
							('3','Counseling Process'),
							('4','Examination Department'),
							('5','Finance Executive'),
							('6','Security Guard'),
							('7','Attendance Process'),
						  ])

	question=fields.Text('Questions')


class SurveyAuditingQuestions(models.Model):
	_name = 'survey.questions'

	name=fields.Selection([('student','Student'),
							('employee','Employee')
						  ])
	student_queston=fields.Selection([('1','Course Survey'),
										('2','Classes for the term'),
										('3','Materials'),
										('4','Employee'),
										('5','Campus Environment'),
										('6','Trainers')],string='Question Type')
	employee_question=fields.Selection([('1','About Muslim English Language'),
										('2','Manager'),
										('3','Enablement'),
										('4','Alignment'),
										('5','Development')],string='Question Type')

	survey_lines_id=fields.One2many('survey.questionslines','survey_lines')
	
	# @api.onchange('student_queston')
	# def get_student_type(self):
	# 	if self.student_queston:
	# 		for x in self.survey_lines_id:
	# 			question_type = dict(self._fields['student_queston'].selection).get(self.student_queston)
	# 			x.question_type=question_type
	
class SurveyAuditingQuestionsLines(models.Model):
	_name = 'survey.questionslines'

	question=fields.Text('Questions')
	question_type=fields.Char('Question Type')
	survey_lines=fields.Many2one('survey.questions')













	




	

	
	