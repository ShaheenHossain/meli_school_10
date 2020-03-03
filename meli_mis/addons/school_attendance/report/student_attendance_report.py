from datetime import timedelta
from dateutil.relativedelta import relativedelta
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class student_attendace_report(models.AbstractModel):
    _name = 'report.school_attendance.student_attendace_report'
    
    @api.multi
    def _get_student_name(self,stud_id):
        print ("==========self.env['student.attendance.report'].browse(stud_id).student_id.name=======",self.env['student.attendance.report'].browse(stud_id))
        return self.env['student.attendance.report'].browse(stud_id).student_id.name
    @api.model
    def render_html(self, docids, data=None):
        Report = self.env['report']
        holidays_report = Report._get_report_from_name('school_attendance.student_attendace_report')
        print ("================self.ids",self.ids)
        print ("================form",data)
        holidays = self.env['hr.holidays'].browse(self.ids)
        docargs = {
            'doc_ids': self.ids,
            'doc_model': 'daily.attendance.line',
            'docs': self.env['daily.attendance.line'].browse(data.get('form')),
            'get_student_name': self._get_student_name(data.get('context').get('active_id')),
#             'get_day': self._get_day(data['form']['date_from']),
#             'get_months': self._get_months(data['form']['date_from']),
#             'get_data_from_report': self._get_data_from_report(data['form']),
#             'get_holidays_status': self._get_holidays_status(),
        }
        return Report.render('school_attendance.student_attendace_report', docargs)