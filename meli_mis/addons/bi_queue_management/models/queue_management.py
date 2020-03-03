from openerp import api, fields, models, _
from odoo.exceptions import UserError, AccessError  
from datetime import datetime, timedelta
from datetime import date, datetime
import dateutil.parser
import urllib2
import json
import pytz

class BiQueueManagement(models.Model):
	_name = 'bi.queue.management'

	name = fields.Char("Name")
	token_id = fields.One2many('bi.token.management', 'department_id', "Token")
	no_token_employee = fields.Integer("Tokens Issued")
	counter_id = fields.Many2one('counter.master', "Counter")	

	@api.multi
	def close_dialog(self):
		return {'type': 'ir.actions.act_window_close'}


class BiTokenManagement(models.Model):
	_name = 'bi.token.management'

	department_id = fields.Many2one("bi.queue.management", "Department")
	user_id = fields.Many2one('res.users', "User", default=lambda self: self.env.user)
	name = fields.Char("Name")
	phone = fields.Char("Phone Number")
	date = fields.Date("Date", default=lambda self: fields.Datetime.now())
	pid = fields.Char('Token No', required=True,
					  default=lambda self: _('New'),
					  help='Personal IDentification Number')
	counter_id = fields.Many2one('counter.master', string="Counter")
	state = fields.Selection([('draft', 'Draft'), ('generate', 'Generate'), ('process', 'Processing'), ('close', 'Close')], index='true', default='draft')
	# video_id = fields.Many2one('youtube.video.link', "Youtube")

	@api.multi
	def generate_token(self):
		date_today= self.date
		token_obj=self.env['bi.token.management']
		date=datetime.today().strftime("%Y-%m-%d")
		app_no=token_obj.search([('date','=',date_today),('department_id','=',self.department_id.id),('state','!=','draft')],count=True)	
		self.pid = str(app_no+1) or _('New')
		self.write({'state':'generate'})
		token = self.env['bi.queue.management'].search([('id','=',self.department_id.id)])
		token.write({'no_token_employee':self.pid})
		# r-eturn {
  #           'type': 'ir.actions.act_window',
  #           'name': 'Token',
  #           'view_type': 'form',
  #           'view_mode': 'form',
  #           'res_model': 'bi.token.management',
  #           'target' : 'inline',
  #           'flags': {'initial_mode': 'edit'}
  #       }


		# return {'target':'inline'}


	@api.multi
	def print_token(self):
		""" Print the invoice and mark it as sent, so that we can see more
			easily the next step of the workflow
		"""
		current_time= datetime.now()
		current_time=current_time.strftime('%Y-%m-%d %I:%M %p')
		user_tz = self.user_id.tz or pytz.utc
		local = pytz.timezone(user_tz)
		current_time = datetime.strftime(pytz.utc.localize(datetime.strptime(str(current_time),"%Y-%m-%d %I:%M %p")).astimezone(local),"%d-%m-%Y %I:%M %p") 
		self.ensure_one()
		self.sent = True
		address = self.env['ip.address.setting'].search([])
		url = 'http://'+address.ip_address+':'+address.port_no+'/hw_proxy/print_xml_receipt'
		data = {
				"jsonrpc": "2.0",
				"params": {"receipt": u'<receipt align="center" font="a" value-thousands-separator="," width="30"><h3>'+self.user_id.company_id.name+'</h3><div>--------------------------------</div><p align="center">Date:'+current_time+'</p><br/><p>Your Token no is generated successfully!!</p><br/><p>Token No:</p><h1>'+self.pid+'</h1><br/><br/><div>--------------------------------</div><p align="left">Please take your seat,we will attain you soon!!</p><div font="a"><br/>' + \
										u'</div></receipt>'},
			}
		req = urllib2.Request(url,json.dumps(data), headers={"Content-Type":"application/json",})
		result = urllib2.urlopen(req)
		# action = self.env.ref('bi_queue_management.action_token_management_tree')
		# result = action.read()[0]
		# res = self.env.ref('bi_queue_management.bi_token_management_form', False)
		# result['views'] = [(res and res.id or False, 'form')]
		# return result

		# context ={
		# 		  'default_name':'',
		# 		  'default_phone':'',
		# 		}
		# return {
		# 		'type': 'ir.actions.act_window',
		# 		'res_model': 'bi.token.management',
		# 		'target' : 'inline',
		# 		'view_mode':'form',
		# 		}
		



	@api.multi
	def set_start(self):
		self.write({'state':'process'})

	@api.multi
	def set_close(self):
		self.write({'state':'close'})


class IpAddressSetting(models.Model):
	_name = 'ip.address.setting'
	_rec_name = 'ip_address'

	ip_address = fields.Char("Ip Address")
	port_no = fields.Char("Port Number")

	@api.model
	def create(self, vals):
		address = self.env['ip.address.setting'].search([])
		if address:
			raise UserError('Please Update the current Ip address and Port Number')
		result = super(IpAddressSetting, self).create(vals)	
		return result	

class YoutubeVideoLink(models.Model):
	_name = 'youtube.video.link'
	_rec_name = 'video_link'

	video_link = fields.Char("Video Link")
	

class CounterMaster(models.Model):
	_name = 'counter.master'

	queue_id = fields.One2many('bi.queue.management','counter_id')
	name = fields.Char("Counter Name")
	user_id = fields.Many2one('res.users', string="Owner")








class CCTvRequest(models.Model):
	_name = 'campus.cctv'


	name=fields.Many2one('hr.employee','Employee Name')
	campus=fields.Many2one('school.school','Campus')
	contact=fields.Char('Contact No')
	designation=fields.Char('Designation')
	image=fields.Binary('Upload File')
	image_filename = fields.Char("Image Filename")
	state=fields.Selection([('draft','Draft'),('request','Complaint'),('close','Closed')],default='draft')
	description=fields.Text('Description')

	@api.onchange('name')
	def getting_employee_details(self):
		if self.name:
			self.campus=self.name.school_id.id
			self.contact=self.name.mobile_phone
			self.designation=self.name.job_id.name


	@api.multi
	def confirm_cc_tv_request(self):
		self.write({'state':'request'})

	@api.multi
	def close_cc_tv_request(self):
		self.write({'state':'close'})


class EmployeeAgreements(models.Model):
	_name ="employee.agreement"

	name=fields.Many2one('hr.employee','Employee Name')
	agreement_name=fields.Char(stirng="Agreement Name")
	image=fields.Binary('Upload File')
	image_filename = fields.Char("Image Filename")
	state=fields.Selection([('draft','Draft'),('confirm','Confirm')],default='draft')


	@api.multi
	def employee_agreement_confirmation(self):
		self.write({'state':'confirm'})


class EmployeePolicies(models.Model):
	_name = 'employee.policy'
	_rec_name="image_filename"

	image=fields.Binary('Upload File')
	image_filename = fields.Char("Image Filename")
	state=fields.Selection([('draft','Draft'),('confirm','Confirm')],default='draft')


	@api.multi
	def employee_policy_confirmation(self):
		self.write({'state':'confirm'})



class CampusesTargets(models.Model):
	_name='admissions.target'

	name=fields.Many2one('school.school',string='Campus', required=True)
	date=fields.Date(string="Date", default=fields.Date.context_today, required=True)
	target_type=fields.Selection([('daily','Daily'),('monthly','Monthly')],string='Target Type')
	months=fields.Selection([(1, 'January'), (2, 'February'), (3, 'March'), (4, 'April'), (5, 'May'), (6, 'June'), (7, 'July'), (8, 'August'), (9, 'September'), (10, 'October'), (11, 'November'), (12, 'December')])
	target=fields.Integer('Target', required=True)

	
	@api.multi
	def target_admissions(self):

		return {
			'type': 'ir.actions.act_window',
			'res_model' : 'admissions.target',
			'view_mode' : 'tree,form',
			'context': {
			        'create':False,
			        'edit' : False,
			        'delete' : False,
			       
			        },
			'nodestroy': True,
		}


class DailyTargetSalesReport(models.TransientModel):
	_name = "daily.sales.report"

	date=fields.Date(string="Select Your Date")
	sales_id=fields.One2many('daily.salelines','line_id')

	@api.onchange('date')
	def getting_sales_target(self):
		self.sales_id=False
		if self.date:
			rec=self.env['school.school'].search([])
			obj=self.env['student.student'].search([])
			rec1=self.env['admissions.target'].search([])
			class_info=[]
			for x in rec:
				pass_students=0
				for y1 in rec1:
					if x.name==y1.name.name and self.date==y1.date:
						class_info.append(({'campus':x.id,'target_achived':pass_students,'campus_actual_targets':y1.target}))
			for i in class_info:
				students=0
				for y in obj:
					if i['campus']==y.school_id.id and y.state=='done' and self.date==y.admission_date:
						students = students+1
				i['target_achived']=students


			self.sales_id=class_info
			for j in self.sales_id:
				for k in rec:
					if j.campus.name==k.name:
						values=(j.target_achived)*(100/j.campus_actual_targets)
						j.remaining=j.campus_actual_targets-j.target_achived
						j.percentage=str(values)+'%'


				
				


	@api.multi
	def getting_print(self):
		self.ensure_one()
		active_ids = self.env.context.get('active_ids', [])
		datas={
		'docs':active_ids,
		'model': 'daily.sales.report',
		'form': self.read()[0]
		}

		return self.env['report'].get_action(self,'bi_queue_management.target_tracker',data=datas)



class AdmissionSalesReportTarget(models.AbstractModel):
	_name = 'report.bi_queue_management.target_tracker'


	@api.model
	def render_html(self, docids, data=None):

		register_ids = self.env.context.get('active_ids', [])
		obj = self.env['daily.sales.report'].search([('id','=',register_ids)])
		target = {}
		count = 1
		for rec in obj.sales_id:
			print len(rec),"2222222222222222222222"
			target[count] = rec.read(['campus','campus_actual_targets','target_achived','remaining','percentage','feedback'])
			count = count + 1

		docargs = {
		'doc_model':'daily.sales.report',
		'data': data,
		'targets':target,
		'docs': register_ids,
		}
		return self.env['report'].render('bi_queue_management.target_tracker', docargs)



	


	

class DailyTargetReportLines(models.TransientModel):
	_name = "daily.salelines"


	campus=fields.Many2one('school.school',string="Campus")
	campus_actual_targets=fields.Integer(string="Daily Sales Target Assignment")
	target_achived=fields.Integer(string="Sales Achieved")
	feedback=fields.Text(string="Feedback By GM")
	remaining=fields.Integer(string='Remaining Achivements',)
	percentage=fields.Char(string='Performence',)
	line_id=fields.Many2one('daily.sales.report')

	# @api.model
	# def _calculate_remaining_achievements(self):
	# 	for x in self:
	# 		values=(x.target_achived)*(100/x.campus_actual_targets)
	# 		self.remaining=x.campus_actual_targets-x.target_achived
	# 		self.percentage=str(values)+'%'







	

			
