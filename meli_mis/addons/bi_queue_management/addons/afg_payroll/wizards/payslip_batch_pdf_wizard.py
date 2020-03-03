from odoo import api, fields, models, _
from odoo.exceptions import UserError


class HrPayslipEmployees(models.TransientModel):
    _name = 'afg.payslipbatch_wizard.pdfreport'

    employee_id = fields.Many2one('hr.afg.payroll.batches', string='Batches', required=True)










