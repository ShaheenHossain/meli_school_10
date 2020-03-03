from odoo import api, fields, models, _
import xlwt, xlsxwriter
import base64


class EmployeeCampusEvaluationExcelReport(models.TransientModel):
    _name = 'employee.campus.evaluation'
    _description = 'Employee Campus Wise Evaluation Excel Report'

    school_id = fields.Many2one('school.school', string='Campus', required=True)

    @api.multi
    def generated_evatluation_excel_report(self, record):
        employee_obj = self.env['hr.emp_appraisal']
        employee_search = employee_obj.search([('campus', '=', self.school_id.name)])
        print employee_search,"11111111111111111"
        workbook = xlwt.Workbook()

        # Style for Excel Report
        style0 = xlwt.easyxf('font: name Calibri, color Black, height 240; align: horiz center; borders: bottom double, right double; pattern: pattern solid, fore_colour light_yellow;', num_format_str='#,##0.00')
        style1 = xlwt.easyxf('font:bold True, color Black , height 400;  borders:top double; align: horiz center; pattern: pattern solid, fore_colour blue;', num_format_str='#,##0.00')
        style2 = xlwt.easyxf('font:bold True, color Black , height 440;  borders:top double; align: horiz center; pattern: pattern solid, fore_colour  gray25;', num_format_str='#,##0.00')
        styletitle = xlwt.easyxf(
            'font:bold True, color White, height 240;  borders: top double; align: horiz center; pattern: pattern solid, fore_colour gray25;',
            num_format_str='#,##0.00')
        sheet = workbook.add_sheet("Employee Evaluation List")

        sheet.write_merge(0, 0, 0, 9, 'Campus Wise Employee Performance Evaluation', style2)

        # sheet.write_merge(1, 1, 0, 5, 'Contact Information', style1)
        # sheet.write_merge(1, 1, 6, 9, 'Position', style1)

        sheet.write(1, 0, 'Name', styletitle)
        sheet.write(1, 1, 'Position', styletitle)
        sheet.write(1, 2, 'Campus', styletitle)
        sheet.write(1, 3, 'HOD/HR/M&E', styletitle)
        sheet.write(1, 4, 'Agreement', styletitle)
        sheet.write(1, 5, 'Salary Remomended', styletitle)
        sheet.write(1, 6, 'Salary Info', styletitle)
        sheet.write(1, 7, 'Last Increment Date', styletitle)
        sheet.write(1, 8, 'Approved by CEO', styletitle)
        sheet.write(1, 9, 'Remark', styletitle)
        
        sheet.col(0).width = 700 * (len('Name'))
        sheet.col(1).width = 700 * (len('Position'))
        sheet.col(2).width = 700 * (len('Campus'))
        sheet.col(3).width = 700 * (len('HOD/HR/M&E'))
        sheet.col(4).width = 700 * (len('Agreement'))
        sheet.col(5).width = 700 * (len('Salary Remomended'))
        sheet.col(6).width = 700 * (len('Salary Info'))
        sheet.col(7).width = 700 * (len('Last Increment Date'))
        sheet.col(8).width = 700 * (len('Approved by CEO'))
        sheet.col(9).width = 700 * (len('Remark'))
        sheet.row(0).height_mismatch = True
        sheet.row(0).height = 256 * 2
        sheet.row(1).height = 256 * 2
        sheet.row(2).height = 256 * 2

        row = 2
        for rec in employee_search:
            sheet.write(row, 0, rec.name.name, style0)
            sheet.write(row, 1, rec.designation, style0)
            sheet.write(row, 2, rec.campus, style0)
            sheet.write(row, 3, rec.average, style0)
            sheet.write(row, 4, '-', style0)
            sheet.write(row, 5, rec.salary_remomended, style0)
            sheet.write(row, 6, rec.salary, style0)
            sheet.write(row, 7, rec.last_increment, style0)
            sheet.write(row, 8, rec.hike, style0)
            sheet.write(row, 9, rec.remark, style0)
            row +=1
        workbook.save('/tmp/employee_campus_list.xls')
        result_file = open('/tmp/employee_campus_list.xls', 'rb').read()
        attachment_id = self.env['wizard.campus.evaluation.excel.report'].create({
            'name': 'Employee Campus Evaluation.xls',
            'report': base64.encodestring(result_file)
        })

        return {
            'name': _('Notification'),
            'context': self.env.context,
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'wizard.campus.evaluation.excel.report',
            'res_id': attachment_id.id,
            'data': None,
            'type': 'ir.actions.act_window',
            'target': 'new'
        }


class WizardEmployeeCampusEvalautionExcelReport(models.TransientModel):
    _name = 'wizard.campus.evaluation.excel.report'

    name = fields.Char('File Name', size=64)
    report = fields.Binary('Prepared File', filters='.xls', readonly=True)
