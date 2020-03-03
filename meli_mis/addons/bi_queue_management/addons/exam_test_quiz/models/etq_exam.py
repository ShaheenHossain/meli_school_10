from openerp import models, fields, api,_
import logging
_logger = logging.getLogger(__name__)
import requests
import time
from openerp.http import request
from datetime import datetime, timedelta, date
from dateutil import relativedelta
from odoo.exceptions import UserError, ValidationError 
from openerp.tools import html_escape as escape, ustr, image_resize_and_sharpen, image_save_for_web
import unicodedata
import re

class EtqExam(models.Model):

    _name = "etq.exam"

    _rec_name="completed_classes"
    
    # name = fields..Many2one('question.question',string="Exam name")
    campus_id=fields.Many2one('school.school',string='Campus')
    program_id=fields.Many2one('standard.standard',string="Program")
    semester_id=fields.Many2one('standard.semester',string="Semester Level")
    exam_date=fields.Date(string='Date of Exam')
    completed_classes=fields.Many2one('school.standard',string="Class")
    name=fields.Many2one('question.question',string="Exam name")
    slug = fields.Char(string="Slug", compute="slug_me", store="True")
    show_correct_questions = fields.Boolean(string="Show Correct Answers?")
    question = fields.One2many('etq.exam.question','exam_ids', string="Questions")
    fill_mode = fields.Selection([('all','All Questions'),('random','Random')], string="Fill Mode", default="all")
    fill_mode_random_number = fields.Integer(string="Number of Random Questions")
    state=fields.Selection([('draft','Draft'),('confirm','Confirmed')],default="draft")
    result_out=fields.Boolean(string="Result Out",default=False)




    @api.constrains('semester_id')
    def semester_validation(self):
        rec = self.env['etq.exam'].search([])

        for obj in rec:
            if obj.id != self.id:
                if obj.program_id == self.program_id and obj.semester_id == self.semester_id and obj.name==self.name:
                    raise UserError(_("Already Exam created "))



    @api.multi
    def exam_status(self):
        self.write({'state':'confirm'})
   

   




    @api.constrains('exam_date')
    def validate_exam(self):
       
        date_time_obj = datetime.strptime(self.exam_date, '%Y-%m-%d')

        all_days=self.all_tuesdays()
        
        
       
        if date_time_obj <= datetime.now():
            raise UserError(_("Please Select after current date"))
      
        
        if self.exam_date  not in all_days:
            raise UserError(_('Exam  Days are Perminent. Please Select Tuesday or  Thursdays'))
       


    def all_tuesdays(self):
        total_days = []
        year = datetime.now().strftime("%Y")    
        d = date(int(year), 1, 1)
        d += timedelta(days = 1 - d.weekday())
        while d.year == int(year):
            total_days.append(str(d))
            d += timedelta(days = 7)

        d1 = date(int(year), 1, 1)
        d1 += timedelta(days = 3 - d1.weekday())
        while d1.year == int(year):
            total_days.append(str(d1))
            d1 += timedelta(days = 7)

       

        return total_days
        


   


    @api.onchange('fill_mode')
    def _onchange_fill_mode(self):
        if self.fill_mode == "random":
            
            rec=self.env['question.question'].search([('program_id','=',self.program_id.name),('semester_id','=',self.semester_id.name)])
            no_questions=[]
            for x in rec:
                for  y in x.questions:
                    no_questions.append(y)
            self.fill_mode_random_number=len(no_questions)


    
    @api.multi
    def view_quiz(self):
        
        quiz_url = request.httprequest.host_url + "exam/" + str(self.slug)
        return {
                'type'     : 'ir.actions.act_url',
                'target'   : 'new',
                'url'      : quiz_url
               } 
       
    @api.one
    @api.depends('name')
    def slug_me(self):
        if self.name:
            s = ustr(self.name)
            uni = unicodedata.normalize('NFKD', s).encode('ascii', 'ignore').decode('ascii')
            slug = re.sub('[\W_]', ' ', uni).strip().lower()
            slug = re.sub('[-\s]+', '-', slug)
           
            
            self.slug = slug

class exam_details(models.Model):
    _name = 'etq.exam.question'

    question=fields.Char(string='Question')
    question_type=fields.Char(string="Question Type")
    options=fields.Char(string="Options")
    correct_options=fields.Char(string="Correct Options")
   
    exam_ids=fields.Many2one('etq.exam',string="Exam id")


class question_paper(models.Model):
    _name="question.question"


    campus_id=fields.Many2one('school.school',string="Campus")
    program_id=fields.Many2one('standard.standard',string="Program")
    semester_id=fields.Many2one('standard.semester',string="Course Level")
    name=fields.Char(string="Exam Name")
    questions = fields.One2many('etq.question','exam_id', string="Questions")
    no_questions=fields.Integer(string="No of Questions")
    pass_marks=fields.Integer(string="Pass Marks")
    time=fields.Char(string="Time")


    @api.onchange('semester_id','program_id')
    def change_exam_name(self):
        for res in self:
            if (res.program_id and res.semester_id):
                res.name=str(res.program_id.code)+'/'+str(res.semester_id.name)


    @api.constrains('semester_id')
    def semester_validation(self):
        rec = self.env['question.question'].search([])

        for obj in rec:
            if obj.id != self.id:
                if obj.program_id == self.program_id and obj.semester_id == self.semester_id:
                    raise UserError(_("Already the Semester name exist"))





    
class EtqQuestion(models.Model):

    _name = "etq.question"
    _rec_name = "question"
    
    exam_id = fields.Many2one('question.question',string="Exam ID")
    image = fields.Binary(string="Image")
    question = fields.Html(string="Question")
    standard_id=fields.Many2one('school.standard',string="Class")
    program_id=fields.Many2one('standard.standard',string="Program")
    semester_id=fields.Many2one('standard.semester',string="Semester Level")

    question_rendered = fields.Html(string="Question Render", compute="render_question", sanitize=False)
    question_type = fields.Selection((('multi_choice','Multiple Choice'), ('fill_blank','Fill in the Blank')), default="multi_choice", string="Question Type")
    question_options = fields.One2many('etq.question.option','question_id',string="Multiple Choice Options")
    question_options_blank = fields.One2many('etq.question.optionblank','question_id',string="Fill in the Blank Options")    
    num_options = fields.Integer(string="Options",compute="calc_options")
    num_correct = fields.Integer(string="Correct Options",compute="calc_correct")

    @api.one
    @api.depends('question')
    def render_question(self):
        if self.question:
            temp_string = self.question
            
            temp_string = temp_string.replace("{1}","<i><input name=\"question" + str(self.id) + "option1\" size=\"5\" style=\"border:none;border-bottom: 1px black solid;\" type=\"text\"/></i>")
            temp_string = temp_string.replace("{2}","<i><input name=\"question" + str(self.id) + "option2\" size=\"5\" style=\"border:none;border-bottom: 1px black solid;\" type=\"text\"/></i>")
            temp_string = temp_string.replace("{3}","<i><input name=\"question" + str(self.id) + "option3\" size=\"5\" style=\"border:none;border-bottom: 1px black solid;\" type=\"text\"/></i>")
            temp_string = temp_string.replace("{4}","<i><input name=\"question" + str(self.id) + "option4\" size=\"5\" style=\"border:none;border-bottom: 1px black solid;\" type=\"text\"/></i>")
            temp_string = temp_string.replace("{5}","<i><input name=\"question" + str(self.id) + "option5\" size=\"5\" style=\"border:none;border-bottom: 1px black solid;\" type=\"text\"/></i>")
            temp_string = temp_string.replace("{6}","<i><input name=\"question" + str(self.id) + "option6\" size=\"5\" style=\"border:none;border-bottom: 1px black solid;\" type=\"text\"/></i>")
            temp_string = temp_string.replace("{7}","<i><input name=\"question" + str(self.id) + "option7\" size=\"5\" style=\"border:none;border-bottom: 1px black solid;\" type=\"text\"/></i>")
            temp_string = temp_string.replace("{8}","<i><input name=\"question" + str(self.id) + "option8\" size=\"5\" style=\"border:none;border-bottom: 1px black solid;\" type=\"text\"/></i>")
            temp_string = temp_string.replace("{9}","<i><input name=\"question" + str(self.id) + "option9\" size=\"5\" style=\"border:none;border-bottom: 1px black solid;\" type=\"text\"/></i>")
            self.question_rendered = temp_string
            
            

    @api.one
    @api.depends('question_options')
    def calc_options(self):
        self.num_options = self.question_options.search_count([('question_id','=',self.id)])
    
    @api.one
    @api.depends('question_options')
    def calc_correct(self):
        self.num_correct = self.question_options.search_count([('question_id','=',self.id), ('correct','=',True)])
    
class EtqQuestionOptions(models.Model):

    _name = "etq.question.option"
    _rec_name = "option"
    
    question_id = fields.Many2one('etq.question',string="Question ID")
    option = fields.Char(string="Option")
    correct = fields.Boolean(string="Correct")
    
class EtqQuestionOptionBlank(models.Model):

    _name = "etq.question.optionblank"
    
    question_id = fields.Many2one('etq.question',string="Question ID")
    answer = fields.Char(string="Blank Answer")



class exam_validation(models.Model):
    _name='exam.exam.validation'


    name=fields.Many2one('student.student',string="Student Name")
    campus_id=fields.Char(string="Campus")
    program_id=fields.Char(string="Program")
    course_level=fields.Char(string="Course Level")
    class_id=fields.Char(string="Class")
    date=fields.Date(string="Date",default=datetime.now())
    marks=fields.Integer(string="No of Questions")
    exam_type=fields.Integer(string="Minimum marks")
    time=fields.Char(string="Time")
    exam = fields.Many2one('etq.exam', string="Exam")


    @api.onchange('name')
    def get_student_details(self):
        if self.name:
            self.campus_id=self.name.school_id.name
            self.program_id=self.name.program_id.name
            self.course_level=self.name.semester_id.name
            self.class_id=self.name.standard_id.standard
            rec=self.env['etq.exam'].search([('program_id','=',self.program_id),('semester_id','=',self.course_level
                )])
            print rec,"555555555555555555"
            self.exam=rec


    @api.onchange('exam')
    def get_exam_details(self):
        rec=self.env['question.question'].search([('name','=',self.exam.name.name)])
        for x in rec:
            self.marks=x.no_questions
            self.exam_type=x.pass_marks
            self.time=x.time





    @api.multi
    def exam_validation_view(self):
            return {
                'type': 'ir.actions.act_window',
                'res_model' : 'exam.exam.validation',
                'view_mode' : 'form',
                
                'target'    : 'inline',
                'nodestroy': True,
                }
        




    @api.multi
    def view_quiz(self):
        


        quiz_url = request.httprequest.host_url + "exam/" + str(self.exam.slug)
        return {
                    'type'     : 'ir.actions.act_url',
                    'target'   : 'new',
                    'url'      : quiz_url
                    } 


    

    




