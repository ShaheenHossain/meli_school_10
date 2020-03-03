from odoo.exceptions import UserError, ValidationError
from odoo import api, fields, models,_

class employee_deciplane(models.Model):
	_name = "hr.employee.deciplane"
	

	@api.multi
	def _get_employee_id(self):
		# assigning the related employee of the logged in user
		active_ids = self.env.context.get('active_ids')
		rec = self.env['hr.employee'].search([('id','=',active_ids[0])])
		return rec.id

	sequence=fields.Integer('Sequence')
	name=fields.Many2one('hr.employee',string="Name",required=True, default=_get_employee_id, readonly=True)
	job_title=fields.Char(string="Job Title")
	mobile=fields.Char(string='Mobile')
	email=fields.Char(string="Email")
	campus=fields.Char(string="Campus")
	department=fields.Char(string="Department")
	status=fields.Selection([('draft','Draft'),('done','Done')])
	diciplane=fields.One2many('hr.employee.diciplane.form','standard',string="Diciplane")
   	

   	@api.multi
   	def confirmation_for_diciplain(self):
   		self.write({'status':'done'})


	@api.onchange('name')
	def get_name_details(self):
		if self.name:
			self.job_title=self.name.job_id.name
			self.mobile=self.name.mobile_phone
			self.email=self.name.work_email
			self.campus=self.name.school_id.name
			self.department=self.name.department_id.name

	


class employee_diciplane_form(models.Model):
	_name = "hr.employee.diciplane.form"
	_order = "sequence"

	sequence=fields.Char('Serial Number')
	diciplane_title = fields.Selection([('verbalcaution','Verbal Caution')
		,('writingwarning','WritingWarning')
		,('verbalwarning','Verbal Warning'),('suspention','Suspention'),
		('decissionmakingleave','Decission Making Leave'),
		('termination','Termination')],string="Diciplain Title")
	description=fields.Char(string="Description")
	date=fields.Date(string="Date")
	standard=fields.Many2one('hr.employee.deciplane')



	# @api.model
	# def create(self, vals):
	# 	print "rrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrr"

	# 	rec = self.env['hr.employee.deciplane'].search([('name.id','=',self.name.id)])
	# 	for obj in rec:
	# 		for diciplain in rec.diciplane:
	# 			print diciplain,"11111111111111"

		# if vals.get('sequence', _('New')) == _('New'):

		# 	print "3333333333333333"
		# 	print vals,"111111111111"

		# 	seq = self.env['hr.employee.deciplane'].search([('standard', '=', vals.get('standard'))],count=True)
		# 	print seq,"0000000000000000000000000000"
		# 	vals['sequence'] = seq+1
		# result = super(employee_diciplane_form, self).create(vals)
		# return result



class hr_employee_diciplane_button(models.Model):
	_inherit = "hr.employee"


	@api.multi
	def hr_employee_deciplane1(self):

		return{
        'type': 'ir.actions.act_window',
        'name':'Employee Deciplane',
        'view_mode': 'tree,form',
        
        'res_model': 'hr.employee.deciplane',
        'domain':[('name','=',self.name)],
    	}


