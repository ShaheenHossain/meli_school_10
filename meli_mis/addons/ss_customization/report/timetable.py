from odoo import models, api
# import calendar
from datetime import datetime
from dateutil.relativedelta import relativedelta as rd


class ReportStudentTimetable(models.AbstractModel):

    _name = 'report.ss_customization.report_student_timetable'


    @api.multi
    def _find_days(self,start_date,end_date):
        print ("=============date",start_date,end_date,type(start_date),type(end_date))
        return (datetime.strptime(end_date, '%Y-%m-%d') - datetime.strptime(start_date, '%Y-%m-%d')).days + 1

    @api.model
    def render_html(self, docids, data):
        print ("=========data",data)
        self.model = self.env.context.get('active_model')
#         docs = self.env[self.model].browse(self.env.context.get('active_ids',
#                                                                 []))
        docargs = {'doc_ids': docids,
                   'doc_model': self.model,
#                    'docs': docs,
                   'data': self.env['school.standard'].browse(data.get('class')),
                   'find_days':self._find_days,
#                    'get_header_data': self.get_header_data,
#                    'get_student': self.get_student,
#                    'daily_attendance': self.daily_attendance
                   }
        print ("============docards",docargs)
        render_model = "ss_customization.report_student_timetable"
        return self.env['report'].render(render_model, docargs)
