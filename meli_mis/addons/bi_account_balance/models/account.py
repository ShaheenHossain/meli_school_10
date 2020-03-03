# -*- coding: utf-8 -*-

from odoo import api, fields, models, tools, SUPERUSER_ID
from odoo.tools.translate import _

#============================================
#class:AccountAccount
#description:debit, credit, balance in chart of account
#============================================

class AccountAccount(models.Model):
    _inherit = "account.account"
    _description = "Account"
    _order = "code"

    #============================================
    #class:AccountAccount
    #method:_find_account_balance
    #description:debit, credit ,balance in chart of account
    #============================================


    @api.depends('account_move_lines')
    def _find_account_balance(self):
        
        for account in self:
            values= self.env['account.move.line'].search([('account_id', '=', account.id),('move_id.state', '=', 'posted')])
            total_debit = 0.0
            total_credit = 0.0
            for value in values:
                if value.debit != 0:
                    total_debit = total_debit + value.amount_currency
                if value.credit != 0: 
                    total_credit = total_credit + value.amount_currency       
            account.update({
                    'credit1': total_credit,
                    'debit1': total_debit,
                    'balance1': total_debit + total_credit,
                })
    account_move_lines = fields.One2many('account.move.line', 'account_id', string='Move Lines', copy=False)
    credit1 = fields.Monetary(string='Credit', readonly=True, compute='_find_account_balance')
    debit1 = fields.Monetary(string='Debit', readonly=True, compute='_find_account_balance')
    balance1 = fields.Monetary(string='Balance', readonly=True, compute='_find_account_balance')


    