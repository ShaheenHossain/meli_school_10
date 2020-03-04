import time
from datetime import datetime, timedelta
from dateutil import relativedelta

import babel
from odoo import api, fields, models, tools, _
from odoo.exceptions import UserError, ValidationError


class VrPayslipBatches(models.Model):
	_name = "hr.afg.payroll.batches"


	name = fields.Char(required=True, readonly=True, states={'draft': [('readonly', False)]})
	slip_ids = fields.One2many('hr.afg.payroll', 'payslip_run_id', string='Payslips', readonly=True,
		states={'draft': [('readonly', False)]})
	company_id = fields.Many2one('res.company',"Company")
	school_id = fields.Many2one('school.school', 'Campus')
	# test = fields.Binary(string="Test")
	state = fields.Selection([
		('draft', 'Draft'),
		('close', 'Close'),
		('done', 'Done'),
		], string='Status', index=True, readonly=True, copy=False, default='draft')
	date_start = fields.Date(string='Date From', required=True, readonly=True,
		states={'draft': [('readonly', False)]}, default=time.strftime('%Y-%m-01'))
	date_end = fields.Date(string='Date To', required=True, readonly=True,
		states={'draft': [('readonly', False)]},
		default=str(datetime.now() + relativedelta.relativedelta(months=+1, day=1, days=-1))[:10])
	credit_note = fields.Boolean(string='Credit Note', readonly=True,
		states={'draft': [('readonly', False)]},
		help="If its checked, indicates that all payslips generated from here are refund payslips.")


	@api.multi
	def draft_payslip_run(self):
		return self.write({'state': 'draft'})

	@api.multi
	def close_payslip_run(self):
		return self.write({'state': 'close'})

	@api.multi
	def Submit_all_payslips(self):
		for records in self.slip_ids:
			records.conformation_paysip()
		return self.write({'state': 'done'})

	@api.onchange('school_id')
	def onchange_company_id(self):
		ttyme = datetime.fromtimestamp(time.mktime(time.strptime(self.date_end, "%Y-%m-%d")))	
		locale = self.env.context.get('lang') or 'en_US'
		if self.school_id:
			self.name = ('Salary on %s ') % (tools.ustr(babel.dates.format_date(date=ttyme, format='MMMM-y', locale=locale))) + str(self.school_id.name)

