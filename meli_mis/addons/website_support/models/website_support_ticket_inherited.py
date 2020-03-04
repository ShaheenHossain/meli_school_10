from openerp import api, fields, models,_
import re
from odoo.exceptions import ValidationError,UserError
import os, sys



#Developer2 For Online Enquiries
class Enquiries_inherited(models.Model):
	_inherit = ["website.support.ticket"]



	name = fields.Char(string="Name",required=True)
	country = fields.Many2one('res.country',string="Country")
	message = fields.Text(string="Message",required=True)
	ticket_no = fields.Char(string="Enquiry No.",Index= True, default=lambda self:('New'),required=True)
	status = fields.Selection([('draft','Draft'),('followup','Followup'),('add-application','Add-Application')],default="draft")
	campus_name = fields.Many2one('school.school',string="Campus-Name")
	address = fields.Char(string="Address")
	# ids=fields.Char(string='Code',compute='_compute_display_name')




	@api.multi
	def name_get(self):
		res = super(Enquiries_inherited, self).name_get()
		result=[]
		for x in self:
			display_value=""
			display_value += x.name or ""
			display_value += ' ['
			display_value += x.ticket_no or ""
			display_value += ']'
		 	result.append((x.id,display_value))
		return result

	@api.model
	def create(self, vals):
		if vals.get('ticket_no', _('New')) == _('New'):
			vals['ticket_no'] = self.env['ir.sequence'].next_by_code('website.support.ticket') or _('New')
			result = super(Enquiries_inherited, self).create(vals)
			return result





	@api.multi
	def enquiry_status(self):

		self.write({"status":"followup"})
	@api.multi
	def application_status(self):
		self.write({"status":"add-application"})

	@api.constrains('email')
	def email_validating(self):
		for x in self:
			if re.match(r"^[a-zA-Z0-9][\w-]*@[a-zA-Z]+\.[a-zA-Z]{1,3}$",x.email)==None:
				raise ValidationError("Please Provide valid Email Address: %s" % x.email)






	

	
	


















	
	@api.constrains('last_name')
	def name_validation(self):
		for y in self:
			if len(y.last_name)>=3:
				return True
			else:
				raise UserError(_("Your name must be more than 3 Characters"))

	