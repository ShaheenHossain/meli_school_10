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
from datetime import datetime, date
# from xlrd.examples.xlrdnameAPIdemo import book
try:
    import xlwt
except ImportError:
    _logger.debug('Cannot `import xlwt`.')
try:
    import cStringIO
except ImportError:
    _logger.debug('Cannot `import cStringIO`.')
try:
    import base64
except ImportError:
    _logger.debug('Cannot `import base64`.')

class SchoolSchool(models.Model):
    _inherit="school.school"

    email_to = fields.Char('Email To')
    email_from = fields.Char('Email From')
    
class PurchaseOrder(models.Model):
    _inherit="purchase.order"

    book_request_id = fields.Many2one('book.request', "Book Request")

class BookRequest(models.Model):
    _name="book.request"

    def _po_count(self):
        for order in self:
            po_obj = self.env['purchase.order'].search([('book_request_id','=',self.id)])
            self.po_count = len(po_obj)
    


    name = fields.Char('Name', default=lambda self: _('New'), readonly=True)
    qty = fields.Integer('Quantity', default="1")
    school_id = fields.Many2one('school.school', 'Campus', required=True)
    book_id = fields.Many2one('product.product', 'Book', required=True)
    date = fields.Date('Date', default=datetime.today(), readonly=True)
    user_id = fields.Many2one('res.users',required=True,readonly=True, default=lambda self: self._uid)
    state = fields.Selection([('draft','Draft'),('sent_fin_manager','Sent to Finanace Manager'), ('sent_ceo','Sent_to_ceo'), ('approved', 'Approved')], 'State', default="draft")
    po_count = fields.Integer(compute="_po_count", default=0)    
    
    @api.multi
    def action_view_purchase_order(self):
        action = self.env.ref('purchase.purchase_form_action').read()[0]
        book_request_id = self.env['purchase.order'].search([('book_request_id','=',self.id)])
        if len(book_request_id) > 1:
            action['domain'] = [('id', 'in', book_request_id.ids)]
        elif len(book_request_id) == 1:
            action['views'] = [(self.env.ref('purchase.purchase_order_form').id, 'form')]
            action['res_id'] = book_request_id.ids[0]
        else:
            action = {'type': 'ir.actions.act_window_close'}
        print("================action",action)
        return action
        
    
    @api.multi
    def send_req_manager(self):
        self.state = 'sent_fin_manager'

    @api.multi
    def send_req_ceo(self):
        self.state = 'sent_ceo'
        
    @api.multi
    def approve_ceo(self):
        self.state = 'approved'
        partner_id=self.env['res.partner'].search([('name','=', 'Muslim Printing')]).id
        if not partner_id:
            partner_id = self.env['res.partner'].create(
                {
                    'name': 'Muslim Printing',
                    'company_type': 'company',
                    'supplier': True
                 
                }
                ).id 
        purchase_order = self.env['purchase.order'].create({
                    'partner_id':partner_id or False,
                    'date_order':datetime.today(),
                    'school_id':self.school_id.id,
                    'date_planned':datetime.today(),
                    'book_request_id': self.id
            })
        
        po_line = self.env['purchase.order.line'].create({
                    'product_id':self.book_id.id ,
                    'name':self.book_id.name,
                    'product_qty':self.qty,
                    'price_unit':self.book_id.standard_price,
                    'order_id':purchase_order.id,
                    'product_uom':self.book_id.uom_po_id.id,
                    'date_planned':datetime.today(),
            })
        purchase_order.button_confirm()
    
    @api.model
    def create(self, vals):
        if vals.get('name', _('New')) == _('New'):
            vals['name'] = self.env['ir.sequence'].next_by_code('book.request') or _('New')
        result = super(BookRequest, self).create(vals)
        return result


class ClassReporting(models.Model):
    _name="class.reporting"
    
    name = fields.Char('Name', default=lambda self: _('New'), readonly=True)
    teacher_id = fields.Many2one('school.teacher', 'Teacher', required=True)
    date = fields.Date('Date', default=datetime.today())
    reason = fields.Char('Reason')
    class_id = fields.Many2one('school.standard', domain=[('state','=', 'running')], required=True)
    enter_time = fields.Float('Enter Time')
    exit_time = fields.Float('Exit Time')
    
    @api.model
    def create(self, vals):
        if vals.get('name', _('New')) == _('New'):
            vals['name'] = self.env['ir.sequence'].next_by_code('class.reporting') or _('New')
        result = super(ClassReporting, self).create(vals)
        return result
    
    @api.multi
    def _cron_class_reporting(self):
        class_lines = self.search([('date', '=', datetime.today())])
        campus_dict = {}
        for record in class_lines:
            campus_dict.setdefault(record.teacher_id.school_id.name, []).append(record)

        for campus in campus_dict:
            print ("==============campus",campus)
            template = self.env.ref('ss_customization.email_template_daily_reporting')
            template_values = {
            'email_to': self.env['school.school'].search([('name','=', campus)]).email_to,
            'email_from': self.env['school.school'].search([('name','=', campus)]).email_from,
            'email_cc': False,
            'auto_delete': True,
            'subject': campus + 'Daily Reporting',
            'report_name': campus + 'Daily Reporting'
        }
            print ("================template",campus_dict.get(campus))
            print template_values,"@@@@@@@@@@@@@@@@@@@@@@@@@"
            teacher = {}
            for record in campus_dict.get(campus):
                teacher.setdefault(record.teacher_id.name, []).append(record.class_id)
            template.write(template_values)
            template.with_context(teacher=teacher,campus=campus).send_mail(self.id, force_send=True, raise_exception=True)
#             mail_template = self.env['mail.template'].browse(template_id)
#             mail_template.write({'email_to': self.email})
#             #this will trigger the mail
#             if mail_template:
#                mail_template.send_mail(self.id, force_send=True, raise_exception=True)
            
            
                
    


class SchoolTeacher(models.Model):
    _inherit = 'school.teacher'
    
    examiner_program_id = fields .Many2one('standard.standard', "Program")
    examiner_is_shift = fields.Selection(related='examiner_program_id.is_shift', store=True)
    examiner_medium_id = fields.Many2one('standard.medium', 'Shift')
    examiner_semester_id = fields.Many2one('standard.semester', "Course Level")
    examiner_room_no = fields.Many2one('standard.division', "Room No")
    start_time = fields.Datetime(string="Start Date")
    end_time = fields.Datetime(string="End Date")

    def daily_reporting(self):
        print ("================================datetime.today()",datetime.today())
        class_lines = self.env['class.reporting'].search([('teacher_id', '=', self.id), ('date', '=', datetime.today())])
        print ("=====class",class_lines)
        workbook = xlwt.Workbook(encoding="utf-8")
        worksheet = workbook.add_sheet(self.name + "Daily Class Reporting")
        class_id = ','.join(record.class_id.standard for record in class_lines)
        reason = ','.join(record.reason or '' for record in class_lines)
        worksheet.write(0, 0, 'Total Class Attended:')
        worksheet.write(1, 0, 'Class:')
        
        worksheet.write(0, 1, len(class_lines))
        worksheet.write(1, 1, class_id)
        
         
        file_data = cStringIO.StringIO()
        workbook.save(file_data)
        res = self.env['reporting.export'].create({
            'data': base64.encodestring(file_data.getvalue()),
            'name': "Daily Reporting.xls"
        })
        return {
            'type': 'ir.actions.act_window',
            'name': 'Daily Reporting',
            'res_model': 'reporting.export',
            'view_mode': 'form',
            'view_type': 'form',
            'res_id': res.id,
            'target': 'new'
        }



class StudentTimetableRegular(models.Model):
    _name = 'student.timetable.regular'

    start_date = fields.Date('Start Date')
    end_date = fields.Date('End Date')
    campus = fields.Many2one('school.school', 'Campus')
    program_id = fields.Many2one('standard.standard', string="Program")

    def print_report(self):
        data = {}
        class_lines = self.env['school.standard'].search([('school_id', '=', self.campus.id), ('standard_id', '=', self.program_id.id), ('start_date', '=', self.start_date), ('end_date', '=', self.end_date)])
        data['class'] = class_lines.ids
        data['active_model'] = 'school.standard'
        print ("==============class+lines", class_lines.ids)
        return self.env['report'].get_action(self, 'ss_customization.report_student_timetable', data=data)

    def print_report_excel(self):
        class_lines = self.env['school.standard'].search([('school_id', '=', self.campus.id), ('standard_id', '=', self.program_id.id), ('start_date', '=', self.start_date), ('end_date', '=', self.end_date)])
        workbook = xlwt.Workbook(encoding="utf-8")
        worksheet = workbook.add_sheet("TimeTable")
        fields_dict = {}
        worksheet.write(0, 0, 'Teacher')
        worksheet.write(0, 1, 'Class')
        worksheet.write(0, 2, 'Room No')
        worksheet.write(0, 3, 'Semester')
        worksheet.write(0, 4, 'Start Date')
        worksheet.write(0, 5, 'End Date')
        worksheet.write(0, 6, 'Spend Days')
        
        row = 0
        col = 1
        for i in class_lines:
            worksheet.write(col, row, i.teacher_id.name)
            worksheet.write(col, row + 1, i.standard)
            worksheet.write(col, row + 2, i.division_id.name)
            worksheet.write(col, row + 3, i.semester_id.name)
            worksheet.write(col, row + 4, i.start_date)
            worksheet.write(col, row + 5, i.end_date)
            worksheet.write(col, row + 6, (datetime.strptime(self.end_date, '%Y-%m-%d') - datetime.strptime(self.start_date, '%Y-%m-%d')).days + 1)
            col += 1
        file_data = cStringIO.StringIO()
        workbook.save(file_data)
        res = self.env['timetable.export'].create({
            'data': base64.encodestring(file_data.getvalue()),
            'name': "TimeTable.xls"
        })
        return {
            'type': 'ir.actions.act_window',
            'name': 'TimeTable',
            'res_model': 'timetable.export',
            'view_mode': 'form',
            'view_type': 'form',
            'res_id': res.id,
            'target': 'new'
        }


class timetable_export(models.TransientModel):
    _name = "timetable.export"
 
    name = fields.Char('filename', readonly=True)
    data = fields.Binary('file', readonly=True)

class Reporting_export(models.TransientModel):
    _name = "reporting.export"
 
    name = fields.Char('filename', readonly=True)
    data = fields.Binary('file', readonly=True)



class SchoolClassExtend(models.Model):
    _name = 'school.class.extend'

    user_id = fields.Many2one('res.users', "User")
    date_to = fields.Date('Date To')
    date_from = fields.Date('Date From')
    standard_id = fields.Many2one('school.standard', 'Standard')
    reason = fields.Char('Reason')
    name = fields.Char('Name', default=lambda self: _('New'), readonly=True)
    state = fields.Selection([('draft','Draft'),('approve','Approved'), ('reject','Rejected')], 'State', default="draft")
    
    @api.one
    def approve(self):
        print ("==============print")
        self.standard_id.end_date = self.date_from
        self.state = 'approve'
    
    @api.one
    def reject(self):
        self.state = 'reject'
    
    
    @api.model
    def create(self, vals):
        if vals.get('name', _('New')) == _('New'):
            vals['name'] = self.env['ir.sequence'].next_by_code('class.extend') or _('New')
        result = super(SchoolClassExtend, self).create(vals)
        return result
    

class ExtendClass(models.TransientModel):
    _name = "extend.class"

    date = fields.Date('Date')
    reason = fields.Char('Reason')

    @api.multi
    def extend(self):
        self.env['school.class.extend'].create({
                'user_id':self._uid,
                'date_from': self.env[self.env.context.get('active_model')].browse(self.env.context.get('active_id')).end_date,
                'date_to':self.date,
                'reason':self.reason,
                'standard_id':self.env.context.get('active_id')
            })
        self.env[self.env.context.get('active_model')].browse(self.env.context.get('active_id')).end_date = self.date
        


class SchoolStandard(models.Model):
    _inherit = 'school.standard'

    extend_class_history = fields.One2many('school.class.extend', 'standard_id', "Extend Class")
    exam_history = fields.One2many('student.examhistory', 'exam_id')
    talk_history=fields.One2many('talk.history','talk_id')
    oyd_history=fields.One2many('oyd.exam.history','oyd_lines')
    code=fields.Char(string="Code")

    @api.onchange('standard_id')
    def program_code_gets(self):
        if self.standard_id:
            print self.standard_id.code,'1111111111111111'
            self.code=self.standard_id.code

    # @api.multi
    # def _cron_start_stop(self):

    #     running_class_ids = self.search([('start_date', '=', fields.Date.today())])
    #     print running_class_ids,'----------------'
    #     running_class_ids.update({
    #         'state':'running'
    #         })
    #     close_class_ids = self.search([('end_date', '=', fields.Date.today())])
    #     close_class_ids.update({'state':'close'})
    #     return


# class StudentFeedback(models.Model):
#     _name = 'student.feedback'

#     student_id = fields.Many2one('student.student', string="Student")
#     feedback = fields.Text('Feedback')
#     subject = fields.Char('subject')
#     submit_to = fields.Selection([('it', 'It Department'), ('hr', 'HR Department'), ('Graviance', 'Graviance')])
#     type = fields.Selection([('idea', 'Idea'), ('problem', 'Problem'), ('quetion', 'Quetion'), ('praise', 'Praise')])

#     @api.model
#     def default_get(self, vals):
#         print ("=============context", self._context)
#         res = super(StudentFeedback, self).default_get(vals)
#         if self._context.get('active_id'):
#             res['student_id'] = self._context.get('active_id')
#         return res
    
#     @api.multi
#     def send_main_feedback(self):
#         if not self.student_id.email:
#             raise UserError('Please Register your email ID')
#         template_obj = self.env['mail.template'].sudo().search([('name', '=', 'Feedback From Student')], limit=1)
#         print ("===========template_obj", template_obj)
#         str = 'Student Name:' + self.student_id.name + '<br/> Class:' + self.student_id.standard_id.standard + '<br/> Program:' + self.student_id.program_id.name + '<br/> Shift:' + self.student_id.medium_id.name + '<br/> Feedback:' + self.feedback + '</td></tr></table>'
#         emails = []
#         users = self.env['student.feedback.setting'].search([], limit=1, order='id desc')
#         if users.user_ids:
#             for email in users.user_ids:
#                 emails.append(email.partner_id.email)
        
#             if template_obj:
#              mail_values = {
#               'subject': template_obj.subject,
#               'body_html': str,
#               'email_to':",".join(emails),
#               'email_from': self.env['res.users'].browse(self._uid).partner_id.email
#              }
#              create_and_send_email = self.env['mail.mail'].create(mail_values).send()  
#              print ("==============create_and_send_email", create_and_send_email)
#         else:
#             raise UserError('Configuration email does not added contact to your administaration')


class StudentFeedbackSetting(models.Model):
    _name = 'student.feedback.setting'

    @api.model
    def default_get(self, vals):
        search = self.search([], limit=1, order='id desc')
        res = super(StudentFeedbackSetting, self).default_get(vals)
        print ("==============search", search)
        if search:
            res['user_ids'] = search.user_ids.ids
        return res

    user_ids = fields.Many2many('res.users')

class OneYearExamHistory(models.Model):
    _name='oyd.exam.history'

    name=fields.Many2one('student.student',string="Students Name",readonly=True)
    f_name=fields.Char(string="F/Name",readonly=True)
    written=fields.Integer(string="Written")
    oral=fields.Integer(string="Oral")
    total=fields.Integer(string="Total",)
    percentage=fields.Char(string='Percentage',)
    grade=fields.Char(string="Grade",)
    oyd_lines=fields.Many2one('school.standard')
    result=fields.Char(string="Results",)



class ExamHistory(models.Model):
    _name="student.examhistory"

    s_name=fields.Many2one('student.student',string="Student Name")
    subject=fields.Char(string="Subject")
    m_term=fields.Integer(string="Middterm")
    written=fields.Integer(string="Written")
    oral=fields.Integer(string="Oral")
    practical=fields.Integer(string="Practical")
    evalution=fields.Integer(string="Class Evaluation")
    makeup=fields.Integer(string="MakeUp")
    total=fields.Integer(string="Total")
    percentage=fields.Char(string="Percentage")
    grade=fields.Char(string="Grade")
    result=fields.Char(string="Results")
    exam_id=fields.Many2one('school.standard')


class Talk_N_Talk_Exam(models.Model):
    _name='talk.history'

    s_name=fields.Many2one('student.student',string="Student Name")
    subject=fields.Char(string="Subject")
    written=fields.Integer(string='Writen Test')
    speaking=fields.Integer(string="Speaking Test")
    total=fields.Integer(string="Total")
    percentage=fields.Char(string="Percentage")
    p_written=fields.Integer(string="P-Written")
    p_speaking=fields.Integer(string="P-Speaking")
    grade=fields.Char(string="Grade")
    result=fields.Char(string="Results")
    talk_id=fields.Many2one('school.standard')


   
        
