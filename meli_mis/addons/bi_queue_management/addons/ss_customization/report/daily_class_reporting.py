from odoo import models, api
# import calendar
from datetime import datetime
from dateutil.relativedelta import relativedelta as rd
from macpath import join


class DailyClassReporting(models.AbstractModel):

    _name = 'report.ss_customization.daily_class_reporting'


    def get_total_class(self,teacher):
        return len(self.env.context.get('teacher')[teacher])
    
    def get_classes(self,classes):
        print ("=========classses",self.env.context.get('teacher').get(classes))
        return (",".join(a.standard for a in self.env.context.get('teacher').get(classes)))

    @api.model
    def render_html(self, docids, data):
        print ("=========data",data)
        print ("=========self",self)
        print ("=========docids",docids)
        print ("=========Context",self.env.context)
        self.model = self.env.context.get('active_model')
#         docs = self.env[self.model].browse(self.env.context.get('active_ids',
#                                                                 []))
        docargs = {'doc_ids': docids,
                   'doc_model': self.model,
#                    'docs': docs,
                'data': self.env.context.get('teacher'),
                'campus': self.env.context.get('campus'),
                'total_class':self.get_total_class,
                'classes':self.get_classes,
                   #'find_days':self._find_days,
#                    'get_header_data': self.get_header_data,
#                    'get_student': self.get_student,
#                    'daily_attendance': self.daily_attendance
                   }
        print ("============docards",docargs)
        render_model = "ss_customization.daily_class_reporting"
        return self.env['report'].render(render_model, docargs)
