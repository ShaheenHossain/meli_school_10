from openerp import models, fields, api
import logging
_logger = logging.getLogger(__name__)
import requests
from openerp.http import request
from datetime import datetime
from openerp.tools import html_escape as escape, ustr, image_resize_and_sharpen, image_save_for_web
import unicodedata
import re

class etq_results(models.Model):

    _name = "etq.result"
    _description = "Exam Result"
    
    exam_id = fields.Many2one('etq.exam', string="Exam", readonly=True)
    name = fields.Many2one('res.users', string="User")
    class_id=fields.Char(string="grade",compute="_compute_grade_calculations")
    score = fields.Char(string="Score", compute="_compute_score")
    results = fields.One2many('etq.result.question', 'result_id', string="Results", readonly=True)
    token = fields.Char(string="Token")
    percentage=fields.Char(string="Percentage",compute="_compute_score")
    state = fields.Selection([('incomplete','In Process'), ('complete','Complete'),('confirm','Confirm')], string="State")
    classes=fields.Char(string="Class",compute="_get_student_class")
    status=fields.Selection([('draft','Draft'),('confirm','Confirm')],default="draft")
    viva_voice=fields.Integer(string="Viva- Voice (%)")

    @api.multi
    def confirm_action(self):
        self.write({'status':'confirm'})



    @api.one
    @api.depends('results')
    def _compute_score(self):
        num_questions = self.env['etq.result.question'].search_count([('result_id', '=', self.id)])
        correct_questions = self.env['etq.result.question'].search_count([('result_id', '=', self.id), ('correct', '=', True)])
        if num_questions > 0:
            self.score = str(correct_questions) + "/" + str(num_questions)

            self.percentage=str( float( float(correct_questions) / float(num_questions) ) * 100) 
            
            # rec=self.env['grade.master'].search([('name','=',self.exam_id.program_id.name)])
            # for x in rec:
            #     print "44444444444444444"
            #     for y in x.grade_ids:
            #         # if y.from_mark < self.percentage:
            #         print float(y.to_mark),'<',self.percentage
            #         if float(y.to_mark) > self.percentage:
            #             print y.grade,'11111111111111111111111111111'
                    
                
        else:
            self.score = str(correct_questions) + "/" + str(num_questions) 

    @api.one
    @api.multi
    @api.depends('percentage')
    def _compute_grade_calculations(self):

        rec=self.env['grade.master'].search([('name','=',self.exam_id.program_id.name)])

        for obj in rec.grade_ids:
            
            # if float(self.percentage) <= float(obj.from_mark) and :
            if float(self.percentage) >= float(obj.from_mark) and float(self.percentage) <= float(obj.to_mark):
                self.class_id = obj.grade
                print obj.grade,"2222222222222222"




    @api.depends('name')
    def _get_student_class(self):

        rec=self.env['student.student'].search([('name','=',self.name.name)])
        self.classes=rec.standard_id.standard
            



        


   


           


class etq_result_question(models.Model):

    _name = "etq.result.question"
    _description = "Exam Result Question"
    
    result_id = fields.Many2one('etq.result', string="Result", readonly=True)
    question = fields.Many2one('etq.question', string="Question", readonly=True)
    question_options = fields.One2many('etq.result.question.option','question_id',string="Options", readonly=True)
    correct = fields.Boolean(string="Correct", readonly=True)
    question_name = fields.Html(related="question.question", string="Question")
    
class etq_result_question_options(models.Model):

    _name = "etq.result.question.option"
    _desciption = "Exam Result Question Option"
    
    question_id = fields.Many2one('etq.result.question',string="Question ID", readonly=True)
    option_id = fields.Many2one('etq.question.option', string="Option", readonly=True)
    option_name = fields.Char(related="option_id.option", string="Option")
    question_options_value = fields.Char(string="Option Value", readonly=True)


class student_send_results(models.Model):
    _name='student.results'

    exam=fields.Many2one('etq.exam',string="Class")


    @api.multi
    def student_class(self):
        rec=self.env['etq.result'].search([('classes','=',self.exam)])
        for obj in rec:
            obj.confirm_action()

        self.exam.result_out = True



   



