# -*- coding: utf-8 -*-
##############################################################################
#
#    This module uses OpenERP, Open Source Management Solution Framework.
#    Copyright (C) 2017-Today Sitaram
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>
#
##############################################################################

from odoo import models, fields, api, _
from odoo.exceptions import UserError
import datetime
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT


class PurchaseOrder(models.Model):
    _inherit="purchase.order"

    material_request_id = fields.Many2one('material.request','Material Request')
    
    @api.model
    def default_get(self,fields):
        print ("=========self._context",self._context)
        res = super(PurchaseOrder, self).default_get(fields)
        if self._context.get('active_id'):
            request_id = self.env['material.request'].browse(self._context.get('active_id'))
#             line_create = []
#             for line in request_id.material_line_ids:
#                 line_create.append((0,0,{'product_id':line.product_id.id,'name':line.product_id.display_name,'product_qty':line.quantity, 'date_planned':datetime.datetime.today().strftime(DEFAULT_SERVER_DATETIME_FORMAT), 'price_unit':1}))
#             print("========line+_create",line_create)
            res.update({
                'school_id':request_id.school_id.id,
                'company_id':request_id.company_id.id,
                'material_request_id':self._context.get('active_id')
#                 'order_line':line_create
                })
            
            
        return res



class StockPicking(models.Model):
    _inherit="stock.picking"

    material_request_id = fields.Many2one('material.request','Material Request')



class MaterialRequest(models.Model):
    _inherit="material.request"

    warehouse_id = fields.Many2one('stock.warehouse','Warehouse', required=True)
    company_id = fields.Many2one('res.company','Company', required=True)
    picking_ids = fields.One2many('stock.picking','material_request_id','Pickings')

    @api.multi
    def button_purchase_order(self):
        return {
            'name': _('Purchase Order'),
            'view_type': 'form',
            'view_mode': 'tree,form',
            'res_model': 'purchase.order',
            'view_id': False,
            'type': 'ir.actions.act_window',
            'domain': [('material_request_id', 'in', self.ids)],
        }

#     @api.multi
#     def done_transfer(self):
#         picking = self.env['stock.picking']
#         picking_type = self.env['stock.picking.type'].search([('warehouse_id','=',self.warehouse_id.id),('code','=','internal')])
#         if not picking_type:
#             raise UserError(_('Configuration Error: please make internal transfer picking type for warehouse'))
#         pick = picking.create({
#             'school_id':self.school_id.id,
#             'location_id': self.location_id.id,
#             'location_dest_id':self.location_dest_id.id,
#             'move_type':'direct',
#             'picking_type_id':picking_type.id,
#             'company_id':self.company_id.id,
#             'material_request_id':self.id
#             })
#         for a in self.material_line_ids:
#             self.env['stock.move'].create({
#                     'product_id':a.product_id.id,
#                     'name':a.product_id.partner_ref,
#                     'product_uom_qty':a.quantity,
#                     'product_uom':a.unit_of_measure.id,
#                     'location_id':pick.location_id.id,
#                     'location_dest_id':pick.location_dest_id.id,
#                     'picking_type_id': pick.picking_type_id.id,
#                     'picking_id':pick.id
#                 })
#         pick.action_confirm()








class InventoryInherited(models.Model):
    _inherit = 'product.template'

    types=fields.Selection([('it','IT'),('consumable','Consumable'),('general','General')],string='Product Type')
    s_no=fields.Integer(string='Serial No')