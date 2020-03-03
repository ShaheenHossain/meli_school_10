

# -*- coding: utf-8 -*-
from datetime import datetime,timedelta
from openerp.exceptions import ValidationError,UserError
from odoo import models, fields, api,_


class timetable_view_classes(models.Model):
	_name='student.classes'

	name=fields.Many2one('standard.standard')
	#name=fields.Selection([('oneyeardiploma','One Year Diploma'),('twoyeardiploma','Two Year Diploma'),('talkntalk','Talk N Talk')])
	course_level=fields.Many2one('standard.semester',string="Course Level")
	classes=fields.Many2one('school.standard',string="Class")
	classes_id=fields.One2many('student.regular.timetable','timetable_id')
	campuses=fields.Many2one('school.school',string='Campus')
	state=fields.Selection([('draft','Draft'),('confirm','Confirmed')],default='draft')
	start_date=fields.Date(string="Class Start Date")
	end_date=fields.Date(string="Class End Date")
	status=fields.Char(string=" Class Status")
	s_no=fields.Integer(string="S.No")


	
	@api.onchange('classes_id')
	def _get_s_no(self):
		self.s_no = len(self.classes_id)+1


	@api.onchange('classes')
	def get_class_dates(self):
		if self.classes:
			self.start_date=self.classes.start_date
			self.end_date=self.classes.end_date
			self.status=self.classes.state


	@api.multi
	def confirmed_class(self):
		self.write({'state':'confirm'})



	@api.multi
	@api.constrains('classes_id')
	def _check_lecture(self):
		domain = [('timetable_id', 'in', self.ids)]
		line_ids = self.env['student.regular.timetable'].search(domain)
		for rec in line_ids:
			records = [rec_check.id for rec_check in line_ids

	
			if (
                rec.teacher_start_time == rec_check.teacher_start_time or
                rec.teacher_end_time == rec_check.teacher_end_time 

                              )]
			if len(records) > 1:
				print "ttttttttttttttttttttt"
				print records,"666666666666666666666666666666"
				raise ValidationError(_('''You cannot set lecture at same
                                            time %s  at same day. 
                                         ''') % (rec.teacher_start_time
                                                        
                                                    ))

                # Checks if time is greater than 24 hours than raise error
            # if rec.start_time > 24:
            #     raise ValidationError(_('''Start Time should be less than
            #                                 24 hours!'''))
            # if rec.end_time > 24:
            #     raise ValidationError(_('''End Time should be less than
            #                                 24 hours!'''))
        	return True



	@api.constrains('classes')
	def check_class_in_time_table(self):
		for x in self:
			rec=self.env['student.classes'].search([('id', '<', x.id)])
			
			for x in rec:
				print self.classes.standard,'111111111111111111'

				if self.classes.standard==x.classes.standard:
					print x.classes.standard
					raise UserError(_('This class is already created '))
		return True
	





	


			
class timetable_for_student(models.Model):
	_name="student.regular.timetable"


	serial_no=fields.Integer(string="Serial No")
	teacher = fields.Many2one('school.teacher', 'Teacher',ondelete='cascade')
	subject = fields.Many2one('student.subjects', 'Subject',ondelete='cascade')

	teacher_start_time = fields.Char("Period Start Time")
	teacher_end_time = fields.Char("Period End Time")
	timetable_id=fields.Many2one('student.classes','Timetable',ondelete='cascade')
	substistute=fields.Many2one('school.teacher',string='Substistute Teacher')
	# substistute_date=fields.Date(string="Date")
	course_level=fields.Many2one('standard.semester',string="Course Level")
	classes=fields.Many2one('school.standard',string="Class")
	campuses=fields.Many2one('school.school',string='Campus')
	name=fields.Many2one('standard.standard')
	start_date=fields.Date(string="Class Start Date")
	end_date=fields.Date(string="Class End Date")
	status=fields.Char(string=" Class Status")
	classes=fields.Many2one('school.standard',string="Class")



	
			



class fee_details_inherited(models.Model):
	_inherit='account.invoice'

	date_of_invoice=fields.Datetime(string="Invoice Date",default=datetime.now())
	date_of_due=fields.Datetime(string='Due-Date')

	

class tyd_class_timetable(models.Model):
	_name='tyd.timetable'


	campuses=fields.Many2one('school.school',string='Campus',required=True)
	name=fields.Many2one('standard.standard',string="Program",required=True)
	course_level=fields.Many2one('standard.semester',string="Course Level",required=True)
	classes=fields.Many2one('school.standard',string="Class",required=True)
	class_id=fields.Char(string='Class',states={'draft': [('invisible', False)]})
	shift_id=fields.Many2one('standard.medium',string="Shift",required=True)
	room_number=fields.Char(string="Room Number",required=True)
	state=fields.Selection([('draft','Draft'),('confirm','Confirmed')],default='draft')
	saturday_id=fields.One2many('tyd.weekdays','period2',string="Days")
	
	pro=fields.Char(string='Code')


	@api.multi
	def timetable_confirmation(self):
		if self.classes:
			self.class_id=self.classes.standard
			rec=self.env['school.standard'].search([])
			rec1=self.env['tyd.teacher.timetable'].search([])
			for x in rec:
				for y in rec1:
					if y.classes.standard==x.standard:
						x.user_id=y.teacher.id
					
			self.write({'state':'confirm'})


	@api.onchange('classes','name')
	def get_room(self):
		self.pro=self.name.code
		if self.classes:
			self.room_number=self.classes.division_id.name

class tyd_weekdays(models.Model):
	_name="tyd.weekdays"

							
	name=fields.Selection([('all','Saturday-Thursday'),
							('saturday','Saturday'),
							 ('sunday','Sunday'),
							 ('monday','Monday'),
							 ('tuesday','Tuesday'),
							 ('wednesday','Wednesday'),
							 ('thursday','Thursday')])
	program=fields.Many2one('standard.standard',string="Program",required=True)
	course_level=fields.Many2one('standard.semester',string="Course Level")
	campuses=fields.Many2one('school.school',string='Campus')
	classes=fields.Many2one('school.standard',string="Class")
	shift_id=fields.Many2one('standard.medium',string="Shift")
	room_number=fields.Char(string="Room Number")

	period3=fields.One2many('tyd.teacher.timetable','periods')
	period2=fields.Many2one('tyd.timetable',ondelete="cascade")
	pro=fields.Char(string='Code')
	period5=fields.Selection([('1st Period','1st Period'),
							 ('2nd Period','2nd Period'),
							 ('3rd Period','3rd Period'),
							 ('4th Period','4th Period'),
							 ('5th Period','5th Period'),
							 ('6th Period','6th Period'),
							 ('7th Period','7th Period')
							 ])
	period6=fields.Selection([('1st Period','1st Period'),
							 ])
	oyd_periods=fields.Selection([('1st Period','1st Period'),
							 	  ('2nd Period','2nd Period'),])


	@api.onchange('name')
	def _get_all_periods(self):
		if self.name:
			values=[]
			if self.pro=='DEL':
				if self.course_level.code in ('PB','SB'):
					kay_val_dict = dict(self._fields['period6'].selection)
					for key, val in kay_val_dict.items():
						ele={
							'period':val,
							'course_level':self.course_level.id,
							'campuses':self.campuses.id,
							'shift_id':self.shift_id.id,
							'classes':self.classes.id,
							'room_number':self.room_number,
							'name':self.name

							}
						values.append(ele)
					self.period3=values
				else:
					kay_val_dict = dict(self._fields['oyd_periods'].selection)
					for key, val in kay_val_dict.items():
						ele={
							'period':val,
							'course_level':self.course_level.id,
							'campuses':self.campuses.id,
							'shift_id':self.shift_id.id,
							'classes':self.classes.id,
							'room_number':self.room_number,
							'name':self.name

							}
						values.append(ele)
					self.period3=values



			if self.pro=='TYD':
				kay_val_dict = dict(self._fields['period5'].selection)
				for key, val in kay_val_dict.items():
					ele={
						'period':val,
						'course_level':self.course_level.id,
						'campuses':self.campuses.id,
						'shift_id':self.shift_id.id,
						'classes':self.classes.id,
						'room_number':self.room_number,
						'name':self.name

						}
					values.append(ele)
				self.period3=values
			if self.pro=='TT' or self.pro=='LADO':
				kay_val_dict = dict(self._fields['period6'].selection)
				for key, val in kay_val_dict.items():
					ele={
						'period':val,
						'course_level':self.course_level.id,
						'campuses':self.campuses.id,
						'shift_id':self.shift_id.id,
						'classes':self.classes.id,
						'room_number':self.room_number,
						'name':self.name,
						'teacher':self.classes.user_id.id
						}
					values.append(ele)
				self.period3=values


	
			

class tyd_saturday_timetable(models.Model):
	_name='tyd.teacher.timetable'

	


	period=fields.Char(string='Period',store=True)
	
	pro=fields.Char(string="Code")

	name=fields.Selection([('all','Saturday-Thursday'),
							 ('saturday','Saturday'),
							 ('sunday','Sunday'),
							 ('monday','Monday'),
							 ('tuesday','Tuesday'),
							 ('wednesday','Wednesday'),
							 ('thursday','Thursday')],readonly=True)
	course_level=fields.Many2one('standard.semester',string="Course Level")
	campuses=fields.Many2one('school.school',string='Campus')
	classes=fields.Many2one('school.standard',string="Class")
	shift_id=fields.Many2one('standard.medium',string="Shift")
	room_number=fields.Char(string="Room Number")
	periods=fields.Many2one('tyd.weekdays',ondelete="cascade")
	subject = fields.Many2one('student.subjects', 'Subject')
	teacher = fields.Many2one('school.teacher', 'Teacher')


	

	

class Substistute_Teacher_Process(models.Model):
	_name = 'teacher.substistute'

	campuses=fields.Many2one('school.school',string='Campus')
	name=fields.Many2one('standard.standard',string="Program")
	course_level=fields.Many2one('standard.semester',string="Course Level")
	shift_id=fields.Many2one('standard.medium',string="Shift")
	class_id=fields.Many2one('school.standard',string="Class")
	day=fields.Selection([('saturday','Saturday'),
							 ('sunday','Sunday'),
							 ('monday','Monday'),
							 ('tuesday','Tuesday'),
							 ('wednesday','Wednesday'),
							 ('thursday','Thursday')],string="Day")
	date=fields.Date(string="Date")
	s_ids=fields.One2many('substistute.teacher','s_id')


	@api.onchange('day','date')
	def teacher_timetable_process(self):
		rec=self.env['tyd.timetable'].search([])
		for x in rec:
			for y in x.saturday_id:
				if self.class_id.standard==x.classes.standard and self.day==y.name:
					var_list=[]
					for z in y.period3:
						ele={
							'period':z.period,
							'subject':z.subject.name,
							'teacher':z.teacher.id,
							'course_level':self.course_level,
							'class_id':self.class_id,
							'shift_id':self.shift_id,
							'day':self.day,
							'date':self.date,

							}
						var_list.append(ele)
					self.s_ids=var_list




class Substistute_teacher(models.Model):
	_name = 'substistute.teacher'

	period=fields.Char(string="Period",readonly=True)
	subject=fields.Char(string="Subject",readonly=True)
	teacher=fields.Many2one('school.teacher',string="Teacher",readonly=True)
	s_teacher=fields.Many2one('school.teacher',string="Substistute Teacher")
	s_id=fields.Many2one('teacher.substistute',ondelete='cascade')
	course_level=fields.Many2one('standard.semester',string="Course Level")
	shift_id=fields.Many2one('standard.medium',string="Shift")
	class_id=fields.Many2one('school.standard',string="Class")
	day=fields.Selection([('saturday','Saturday'),
							 ('sunday','Sunday'),
							 ('monday','Monday'),
							 ('tuesday','Tuesday'),
							 ('wednesday','Wednesday'),
							 ('thursday','Thursday')],string="Day")
	date=fields.Date(string="Date")



class Classes_Inherited(models.Model):
	_inherit = 'school.standard'

	term=fields.Char(string='Term')
	program_code=fields.Char(string='Code')
	add_final_date=fields.Date(string="Final date")


	@api.onchange('standard_id','start_date')
	def get_program_code(self):
		if self.standard_id:
			self.program_code=self.standard_id.code
		if self.start_date:
			datetime_object = datetime.strptime(self.start_date, '%Y-%m-%d').date()
			coming_day =datetime_object + timedelta(days=1)
			self.add_final_date=coming_day



class CheckingTimetableForTeacher(models.AbstractModel):

	_name = 'timetable.timetable'

	campuses = fields.Many2one('school.school',string='Campus')
	name = fields.Many2one('standard.standard',string="Program")
	shift_id = fields.Many2one('standard.medium',string="Shift")


	t_id = fields.One2many('teacher.timetable.view','teacher_id',string="Class")
	teacher_not_assigned=fields.One2many('notassign.teacher','not_teacher')
	room_id=fields.One2many('room.teacher','r_id')





	@api.onchange('name','course_level','shift_id')
	def get_teacher_details(self):
		
		rec=self.env['tyd.timetable'].search([('campuses','=',self.campuses.name),('name','=',self.name.name),('shift_id','=',self.shift_id.code)])
		obj=self.env['school.teacher'].search([('school_id','=',self.campuses.name)])
		
		teachers=[]
		for x in rec:
			for y in x.saturday_id:
				for z in y.period3:
					fmt = '%Y-%m-%d'
					d1 = datetime.strptime(str(datetime.today().date()), fmt)
					d2 = datetime.strptime(z.classes.end_date, fmt)
					daysDiff = str((d2-d1).days)         
					daysDiff = str((d2-d1).days + 1)   
					
					teachers.append(({'teacher_name':z.teacher.id,
									  'class_id':z.classes.id,
									  'course_level':z.course_level.id,
									  'start_date':z.classes.start_date,
									  'end_date':z.classes.end_date,
									  'available_days':daysDiff+' Days',
									  'room_no':z.classes.division_id.name
									  }))

		self.t_id=teachers

	@api.onchange('shift_id')
	def free_teachers_details(self):
		rec=self.env['school.standard'].search([])
		rec1=self.env['standard.division'].search([])
		obj=self.env['school.teacher'].search([])
		obj1=self.env['tyd.teacher.timetable'].search([])
		rooms=[]
		teachers=[]
		count=0
		s_no=0
		for x in rec:
			if x.school_id.name==self.campuses.name and x.standard_id.name==self.name.name and x.medium_id.code==self.shift_id.code:
				for y in rec1:
					if x.division_id.name!=y.name:
						count+=1
						rooms.append(({'serial_no':count,'room_no':y.name}))
		
		for i in obj:
			for j in obj1:
				if self.campuses.name==j.campuses.name:
					if i.employee_code != j.teacher.employee_code:
						s_no+=1
						teachers.append(({'serial_no':s_no,'teacher_name':i.id}))
		 
		self.teacher_not_assigned=teachers
		self.room_id=rooms




					







					

class GettingTeacherDetails(models.TransientModel):

	_name = 'teacher.timetable.view'


	teacher_name = fields.Many2one('school.teacher',string="Teacher")
	class_id = fields.Many2one('school.standard',string="Class")
	course_level = fields.Many2one('standard.semester',string="Course Level")
	start_date=fields.Date(string="Start Date")
	end_date=fields.Date(string="End Date")
	room_no = fields.Char(string="Room No")
	available_days=fields.Char(string="Remaining Days")
	teacher_id=fields.Many2one('timetable.timetable',ondelete='cascade')


class NotAssignedTeachers(models.TransientModel):
	_name = 'notassign.teacher'

	serial_no=fields.Char(string="Serial No")
	teacher_name=fields.Many2one('school.teacher',string="Teacher Name")
	not_teacher=fields.Many2one('timetable.timetable')


class GettingFreeRooms(models.TransientModel):
	 _name = 'room.teacher'

	 serial_no=fields.Char(string="Serial No")
	 room_no=fields.Char(string="Room No")

	 r_id = fields.Many2one('timetable.timetable')



class UsersClassInherited(models.Model):

	_inherit='res.users'

	campus=fields.Many2one('school.school','Campus')


















		


	




			




	
		

				