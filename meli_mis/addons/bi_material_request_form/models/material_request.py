from datetime import datetime, timedelta, date
from dateutil import relativedelta

from odoo import api, fields, models, tools, SUPERUSER_ID, _
from odoo.exceptions import UserError, AccessError
from ast import literal_eval

class MaterialRequest(models.Model):
	_name = "material.request"
	_description = "Internal Material Request"
	_order = "id desc"
	_inherit = ["ir.needaction_mixin"]


	@api.model
	def _needaction_domain_get(self):
		employee = self.env['hr.employee'].search([])
		for manager in employee:
			if self.env.user.name == manager.name:
				if manager.manager == True:
					return [('state', '=', 'waiting')]

	@api.multi
	def _get_default_picking_type(self):
		
		return self.env['stock.picking.type'].search([('name', '=', 'Internal Transfers')], limit=1).id

	def _get_employee_id(self):
		# assigning the related employee of the logged in user
		employee_rec = self.env['hr.employee'].search([('user_id', '=', self.env.uid)], limit=1)
		return employee_rec.id
	

	name = fields.Char(
		'Sequence', default='/',
		copy=False,  index=True)
	reference = fields.Char(string="Reference")
	state = fields.Selection([
						('draft', 'Draft'),
						('cancel', 'Cancelled'),
						('hod_manager','HOD/Line Manager'),
						('it','IT Department'),
						('procurement','Procurement'),
						('inventory','Inventory Department'),
						('reject','Reject'),
						('pending','Pending'),
						('approved','Approved'),
						('received','Received'),
						('done', 'Issued')
						], string='Status', index= True, default='draft',
						store=True, help=" * Draft: not confirmed yet and will not be scheduled until confirmed\n"
						" * Cancelled: has been cancelled, can't be confirmed anymore")
	location_id = fields.Many2one('stock.location', "Source Location Zone", compute="_get_source_location")
	location_dest_id = fields.Many2one('stock.location', "Destination Location Zone")
	# warehouse_id = fields.Many2one('stock.warehouse', string="Warehouse",select=True, required=False)
	material_line_ids = fields.One2many('material.request.line','material_id',string="Material Request Line")
	# picking_type_id = fields.Many2one('stock.picking.type', string="Stock Picking Type", default=_get_default_picking_type)
	transfer_reference = fields.Many2one('stock.picking',string="Transfer Reference",readonly=True)

	# resignation = fields.Many2one('hr.employee.category',string='Destination')
	# requester_id = fields.Many2one('stock.picking', string="Requester")
	designation = fields.Many2one('hr.job', "Designation", required=True)
	transfer_date = fields.Date(string="Scheduled Date", required=True, default=fields.Datetime.now)
	note = fields.Text(string="Reason")
	department =fields.Many2one('hr.department',string='Department')
	requester = fields.Many2one('hr.employee', "Requester",default=_get_employee_id)
	school_id = fields.Many2one('school.school',string="Campus")
	issued_by = fields.Many2one('res.users', "Issued by")
	technical_team=fields.Selection([('it','IT Department'),('procurement','Procurement')],string='Technical Team')
	line_manager_remark = fields.Text(string="HOD/Manager")
	tech_remark = fields.Text(string="Technical Team")
	inventory_remark = fields.Text(string="Inventory Team")
	condition = fields.Selection([('new','New'),
								('poor','Poor'),
								('good','Good'),
								('very_good','Very Good')], string="Condition")

	@api.depends('requester')
	@api.one
	def _get_source_location(self):
		source_locations = self.env['stock.location'].search([])
		for locations in source_locations:
			if self.school_id == locations.school_id:
				self.location_id = locations.id

	@api.model
	def create(self, vals):
		if vals.get('name', _('New')) == _('New'):
			if 'school_id' in vals:
				vals['name'] = self.env['ir.sequence'].with_context(force_company=vals['school_id']).next_by_code('material.request.new') or _('New')
			else:
				vals['name'] = self.env['ir.sequence'].next_by_code('material.request.new') or _('New')	
				
		result = super(MaterialRequest, self).create(vals)
		return result

	@api.onchange('requester')
	def onchange_requester(self):
		if self.requester:
			self.school_id = self.requester.school_id
			self.department = self.requester.department_id
			self.designation = self.requester.job_id

	def do_confirm(self):
	# self.send_mail_template()
		self.write({'state':'hod_manager'})

	def hod_approve_action(self):
		if self.technical_team == 'it':
			return self.write({'state':'it'})
		if self.technical_team=='procurement':
			return self.write({'state':'procurement'})
		else:
			raise UserError('Please Choose Product Category[Technical Team]')

	def technical_team_approve_action(self):
		self.write({'state':'inventory'})

	def reject_action(self):
		self.write({'state':'reject'})

	def pending_action(self):
		self.write({'state':'pending'})

	@api.multi
	def send_mail_template(self):
		# Find the e-mail template
		template = self.env.ref('bi_material_request_form.material_request_mail')
		# You can also find the e-mail template like this:
		# template = self.env['ir.model.data'].get_object('mail_template_demo', 'example_email_template')
 
		# Send out the e-mail template to the user
		self.env['mail.template'].browse(template.id).send_mail(self.id)

	def done_receive(self):
		self.write({'state':'received'})

	@api.constrains('state')
	def onchange_condition_action(self):
		if self.state == 'done':
			if self.condition == False:
				raise UserError("Plese Select Meterial Condition")
			else:
				pass

	def approve_product(self):
		for vals in self:
			type_obj = self.env['stock.picking.type']
			picking_type_id = type_obj.search([('name', '=', 'Internal Transfers')], limit=1)#,('default_location_src_id','=',vals.location_id.id)
			pick = {
					'origin': vals.name,
					'school_id': vals.school_id.id,
					# 'requester_id': vals.school_id.id,
					'delivery_slip_id': vals.id,
					'picking_type_id': picking_type_id.id,
					'location_id': vals.location_id.id,
					'location_dest_id': vals.location_dest_id.id,
					'min_date': vals.transfer_date,
				}
		picking = self.env['stock.picking'].create(pick)
		for line in self.material_line_ids:
			move = {
				'name': vals.name,
				'product_id': line.product_id.id,
				'product_uom_qty': line.quantity if line.quantity<line.product_id.qty_available else line.product_id.qty_available,
				'product_uom': line.unit_of_measure.id,
				'location_id': vals.location_id.id,
				'location_dest_id': vals.location_dest_id.id,
				'picking_id': picking.id,
				}
			self.env['stock.move'].create(move)
		# for pack in picking.move_lines:
		# 	operation = {
		# 				'product_id': pack.product_id.id,
		# 				'qty_done': pack.product_uom_qty,
		# 				'product_qty': pack.product_uom_qty,
		# 				'location_id': pack.location_id.id,
		# 				'location_dest_id': pack.location_dest_id.id,
		# 				'product_uom_id': pack.product_uom.id,
		# 				'picking_id': picking.id,
		# 	}
		# 	self.env['stock.pack.operation'].create(operation)
		picking.action_assign()
		self.transfer_reference = picking.id

	
	def do_approve(self):
		self.write({'state':'approved'})

	def done_transfer(self):

		product_quant = self.env['stock.quant'].search([])

		for line in self.material_line_ids:
			# if line.product_id.qty_available <= 0:
			quantity = 0
			for quant in product_quant:
				if quant.product_id == line.product_id and quant.location_id == self.location_id:
					quantity = quant.qty
			if quantity <= 0:
				raise UserError(_("Material %s is not available")%line.product_id.name)
			if quantity < line.quantity:
				raise UserError(_("available Quantity is %s")%quantity)

		# if not self.location_id:
		# 	raise UserError(_("Please select source location"))
		# elif not self.location_dest_id:
		# 	raise UserError(_("Please select destination location"))
		self.approve_product()
		transfer = self.env['stock.immediate.transfer'].create({'pick_id': self.transfer_reference.id})
		transfer.process()
		self.write({'state': 'done','issued_by': self.env.user.id})
		asset_obj=self.env['account.asset.asset']
		for line in self.material_line_ids:
			if line.asset_id:
				asset=asset_obj.search([('id','=',line.asset_id.id)])
				asset.write({'custodian':line.material_id.requester.user_id.id,'employee_id':line.material_id.requester.id,'school_id':line.material_id.requester.school_id.id})

class MaterialRequestLine(models.Model):
	_name = 'material.request.line'

	product_id = fields.Many2one('product.product','Product')
	quantity = fields.Float(string="Quantity", default=1.0)
	unit_of_measure = fields.Many2one('product.uom',string="Unit Of Measure")
	product_cost = fields.Float(string="Cost")
	product_unit_price = fields.Float(string="Unit Price")
	material_id = fields.Many2one('material.request',string="Material Request")
	asset_id = fields.Many2one('account.asset.asset',string="Description")
	state = fields.Selection([
		('draft', 'Draft'),('cancel', 'Cancelled'),
		('waiting','Waiting For Approval'),
		('approved','Approved'),
		('received','Received'),
		('done', 'Done')], string='Status', index= True, default='draft', related='material_id.state',
		store=True, help=" * Draft: not confirmed yet and will not be scheduled until confirmed\n"
			 " * Cancelled: has been cancelled, can't be confirmed anymore")

	@api.onchange('product_id')
	def onchange_product_id(self):
		for vals in self:
			if vals.product_id:
				vals.unit_of_measure = vals.product_id.uom_id
				vals.product_cost = vals.product_id.standard_price
				vals.product_unit_price = vals.product_id.list_price 

class Picking(models.Model):
	_inherit = "stock.picking"

	delivery_slip_id = fields.Many2one('material.request',string="Delivery Payslip")
	employee_id = fields.Many2one('hr.employee', string="Employee")

class PurchaseOrderInheritSelection(models.Model):
	_inherit = "purchase.order"

	state = fields.Selection(selection_add=[('create', 'Draft'),
											('gm', 'General management'),
											('top_management', 'Top Management')], default="create")
	topm_remark = fields.Text(string="Top Management Remark")

	@api.constrains('state')
	def topm_remark_validation(self):
		if self.state == "draft":
			if self.topm_remark == False:
				raise UserError('Please add Comment on Top Management Remark')

	@api.multi
	def sendtogm_action(self):
		return self.write({'state': 'gm'})

	@api.multi
	def gm_approve_action(self):
		return self.write({'state': 'top_management'})

	@api.multi
	def gm_cancel_action(self):
		return self.write({'state': 'cancel'})

	@api.multi
	def top_management_approve_action(self):
		return self.write({'state': 'draft'})

	@api.multi
	def top_management_reject_action(self):
		return self.write({'state': 'cancel'})

	@api.multi
	def top_management_pending_action(self):
		pass

class InventoryReoport(models.TransientModel):
	_name = "inventory.report"


	report_type = fields.Selection([('campus_wise','Campus Base'),
									('item_wise','Item Base'),
									('employee_base','Employee Base'),
									('date_base','Date Base')],default='campus_wise')
 
	campus=fields.Many2one('res.company',string="Campus")
	item=fields.Many2one('product.product',string="Product")
	name=fields.Many2one('hr.employee',string="Employee")
	start_date =fields.Date(string="Start Date") 
	end_date =fields.Date(string="End Date")
	on_hand=fields.Boolean(string='On Hand', default=False)
	on_issue=fields.Boolean(string='Issue', default=False)

	inventory_onhand_id=fields.One2many('campus.onhand','onhand_id')
	on_hand_total = fields.Integer(string="Total", readonly=True)


	inventory_issue_id=fields.One2many('campus.issue.products','issue_id')
	issue_product_total = fields.Integer(string="Total",readonly=True)

# Onhand For campus Report

	@api.onchange('report_type')
	def onchange_campus(self):
		if self.report_type:
			self.campus=False
			self.item=False
			self.name=False
			self.start_date=False
			self.end_date=False
			self.on_hand=False
			self.on_issue=False
			self.inventory_onhand_id=False
	@api.onchange('campus')
	def campus_onchange(self):
		if self.campus:
			self.inventory_onhand_id=False
			self.inventory_issue_id=False

	@api.multi
	def Getting_Onhand_Quantity(self):
		self.on_hand=True
		self.on_issue=False
		self.inventory_onhand_id = False
		self.inventory_issue_id=False
		self.on_hand_total = False
		rec=self.env['stock.quant'].search([])
		values = []
		total_qty = 0
		if self.campus:
			for x in rec:
				if self.campus.name==x.location_id.company_id.name and x.location_id.name=="Stock":
					values.append(({'product':x.product_id.id,
									'quantity':x.qty,
									'location':x.location_id.company_id.name,
									'incomig_date':x.in_date,
									'inventory_value':x.inventory_value}))
					total_qty = total_qty + x.qty

		if self.item:
			for x in rec:
				if self.item == x.product_id and x.location_id.name=="Stock":
					values.append(({'product':x.product_id.id,
										'quantity':x.qty,
										'location':x.location_id.company_id.name,
										'incomig_date':x.in_date,
										'inventory_value':x.inventory_value,
										}))
					total_qty = total_qty + x.qty

		if self.start_date and self.end_date:
			purchase_pro = self.env['purchase.order'].search([])

			for x in purchase_pro:
				dates = str(x.date_order)[:10]
				if self.start_date <= dates and self.end_date >= dates:
					values.append(({'product':x.order_line.product_id.id,
									'quantity':x.order_line.product_qty,
									'location':x.school_id.name,
									'incomig_date':x.date_order,
									'inventory_value':x.amount_total,
									}))
					total_qty = total_qty + x.order_line.product_qty

	   	self.inventory_onhand_id = values
	   	self.on_hand_total = total_qty

# Issue Of Product  Report

	@api.multi
	def Getting_Issue_Of_Products(self):
		self.on_issue=True
		self.on_hand=False
		self.inventory_issue_id=False
		self.issue_product_total = False
		self.inventory_onhand_id=False
		rec=self.env['material.request'].search([])
		values = []
		total_issue = 0
		if self.campus:
			for x in rec:
				if self.campus.name==x.location_id.company_id.name and x.state=='done':
					values.append(({'employee':x.requester.id,
									'sequence':x.name,
									'department':x.department.name,
									'campus':x.school_id.name,
									's_date':x.transfer_date,
									'qty':x.material_line_ids.quantity}))
					total_issue = total_issue + x.material_line_ids.quantity

		if self.item:
			for x in rec:
				if self.item == x.material_line_ids.product_id and x.state=='done':
					values.append(({'employee':x.requester.id,
									'sequence':x.name,
									'department':x.department.name,
									'campus':x.school_id.name,
									's_date':x.transfer_date,
									'qty':x.material_line_ids.quantity}))
					total_issue = total_issue + x.material_line_ids.quantity

		if self.name:
			for x in rec:
				if self.name == x.requester and x.state == "done":
					values.append(({'employee':x.requester.id,
									'sequence':x.name,
									'department':x.department.name,
									'campus':x.school_id.name,
									's_date':x.transfer_date,
									'qty':x.material_line_ids.quantity}))
					total_issue = total_issue + x.material_line_ids.quantity

		if self.start_date and self.end_date:
			for x in rec:
				dates = x.transfer_date
				if self.start_date <= dates and self.end_date >= dates:
					values.append(({'employee':x.requester.id,
									'sequence':x.name,
									'department':x.department.name,
									'campus':x.school_id.name,
									's_date':x.transfer_date,
									'qty':x.material_line_ids.quantity}))
					total_issue = total_issue + x.material_line_ids.quantity


	   	self.inventory_issue_id = values
	   	self.issue_product_total = total_issue

	
	@api.multi
	def get_product_total(self):
		self.on_hand=True
		self.on_issue=True
		self.inventory_onhand_id=False
		self.inventory_issue_id=False
		self.on_hand_total = False
		self.issue_product_total = False

		rec=self.env['stock.quant'].search([])
		aval_quantity = []
		total_qty = 0
		total_issue = 0
		if self.campus:
			for x in rec:
				if self.campus.name==x.location_id.company_id.name:
					aval_quantity.append(({'product':x.product_id.id,
										'quantity':x.qty,
										'location':x.location_id.name,
										'incomig_date':x.in_date,
										'inventory_value':x.inventory_value,
										}))
					total_qty = total_qty + x.qty

		if self.item:
			for x in rec:
				if self.item == x.product_id and x.location_id.name=="Stock":
					aval_quantity.append(({'product':x.product_id.id,
										'quantity':x.qty,
										'location':x.location_id.company_id.name,
										'incomig_date':x.in_date,
										'inventory_value':x.inventory_value,
										}))
					total_qty = total_qty + x.qty

		if self.start_date and self.end_date:
			purchase_pro = self.env['purchase.order'].search([])

			for x in purchase_pro:
				dates = str(x.date_order)[:10]
				if self.start_date <= dates and self.end_date >= dates:
					aval_quantity.append(({'product':x.order_line.product_id.id,
									'quantity':x.order_line.product_qty,
									'location':x.school_id.name,
									'incomig_date':x.date_order,
									'inventory_value':x.amount_total,
									}))
					total_qty = total_qty + x.order_line.product_qty

	   	self.inventory_onhand_id = aval_quantity
	   	self.on_hand_total = total_qty

	   	rec=self.env['material.request'].search([])
		issue_pro = []
		if self.campus:
			for x in rec:
				if self.campus.name==x.location_id.company_id.name and x.state=='done':
					issue_pro.append(({'employee':x.requester.id,
									'sequence':x.name,
									'department':x.department.name,
									'campus':x.school_id.name,
									's_date':x.transfer_date,
									'qty':x.material_line_ids.quantity}))
					total_issue = total_issue + x.material_line_ids.quantity
		
		if self.item:
			for x in rec:
				if self.item == x.material_line_ids.product_id and x.state=='done':
					issue_pro.append(({'employee':x.requester.id,
									'sequence':x.name,
									'department':x.department.name,
									'campus':x.school_id.name,
									's_date':x.transfer_date,
									'qty':x.material_line_ids.quantity}))
					total_issue = total_issue + x.material_line_ids.quantity

		if self.start_date and self.end_date:
			for x in rec:
				dates = x.transfer_date
				if self.start_date <= dates and self.end_date >= dates:
					issue_pro.append(({'employee':x.requester.id,
									'sequence':x.name,
									'department':x.department.name,
									'campus':x.school_id.name,
									's_date':x.transfer_date,
									'qty':x.material_line_ids.quantity}))
					total_issue = total_issue + x.material_line_ids.quantity

	   	self.inventory_issue_id = issue_pro
	   	self.issue_product_total = total_issue

	@api.onchange('campus')
	def campus_onchange(self):
		if self.campus:
			self.inventory_issue_id=False
			self.inventory_onhand_id=False

	@api.multi
	def get_print(self):
		self.ensure_one()
		active_ids = self.env.context.get('active_ids', [])
		datas={
		'docs':active_ids,
		'model': 'inventory.report',
		'form': self.read()[0]
		}
		return self.env['report'].get_action(self,'bi_material_request_form.product_tracker',data=datas)

class InventoryProductTracker(models.AbstractModel):
    _name = 'report.bi_material_request_form.product_tracker'

    @api.model
    def render_html(self, docids, data=None):
    	
		register_ids = self.env.context.get('active_ids', [])
		lines_data = self.env['inventory.report'].search([('id','=',register_ids)])

		on_hand={}
		count = 1
		for lines in lines_data.inventory_onhand_id:
			on_hand[count] = lines.read(['product','location','incomig_date',
										'inventory_value','quantity'])
			count = count+1
		print on_hand,"222222222222222222222"

		self_data = {}
		key = 1
		for data in lines_data:
			self_data[key] = data.read(['report_type','campus','item','name','start_date',
										'end_date','on_hand','on_issue'])
			key = key+1
		print self_data,"333333333333333333333"

		issue_pro = {}
		issue_count = 1
		for data in lines_data.inventory_issue_id:
			issue_pro[issue_count] = data.read(['employee','sequence','department','campus','s_date','qty'])
			issue_count = issue_count+1

		print issue_pro,"4444444444444444444444"




		docargs = {
		'doc_model':'inventory.report',
		'data': data,
		'quantity':on_hand,
		'issue':issue_pro,
		'self_data':self_data,
		'docs': register_ids,
		}
		return self.env['report'].render('bi_material_request_form.product_tracker', docargs)





class Onhand_products(models.TransientModel):
	_name ='campus.onhand'

	product =fields.Many2one('product.product',string='Product')
	quantity =fields.Integer('Quantity')
	location = fields.Char('Location')
	incomig_date = fields.Date('Date')
	inventory_value = fields.Float('Inventory Value')
	onhand_id =fields.Many2one('inventory.report')


class Issue_Of_products(models.TransientModel):
	_name ='campus.issue.products'

	employee=fields.Many2one('hr.employee',string="Employee")
	sequence=fields.Char('Sequence')
	department=fields.Char('Department')
	campus=fields.Char('Campus')
	s_date=fields.Date('Scheduled Date')
	qty=fields.Integer(string="Quantity")
	issue_id=fields.Many2one('inventory.report')



