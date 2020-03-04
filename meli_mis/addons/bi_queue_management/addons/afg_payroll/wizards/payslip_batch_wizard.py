from odoo import api, fields, models, _
from odoo.exceptions import UserError


class HrPayslipEmployees(models.TransientModel):
    _name = 'afg.payslipbatch_wizard'
    _description = 'Generate payslips for all selected employees'

    employee_ids = fields.Many2many('hr.employee',string="Employees")


    @api.multi
    def compute_sheet(self):
    	payslips = self.env['hr.afg.payroll']
        [data] = self.read()
        active_id = self.env.context.get('active_id')
        if active_id:
            [run_data] = self.env['hr.afg.payroll.batches'].browse(active_id).read(['date_start', 'date_end'])
        from_date = run_data.get('date_start')
        to_date = run_data.get('date_end')
        if not data['employee_ids']:
            raise UserError(_("You must select employee(s) to generate payslip(s)."))
    	for employee in self.env['hr.employee'].browse(data['employee_ids']):
			res = {
			'employee_id': employee.id,
			'start_date': from_date,
			'end_date': to_date,
			'payslip_run_id': active_id,
			}
			payslips += self.env['hr.afg.payroll'].create(res)
			payslips.get_all_data()
	return {'type': 'ir.actions.act_window_close'}



