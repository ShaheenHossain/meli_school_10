# -*- coding: utf-8 -*-
{
    'name': "school_ems",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "KarimiInfo Tech Pvt Ltd.",
    'website': "http://www.karimiinfotech.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/10.0/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','school','bi_hr','school_fees','mail','exam_test_quiz','school_attendance'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/templates.xml',
        'views/mid_exam_view.xml',
        'views/teacher_inherited_view.xml',
        
        'views/student_reminder_view.xml',
        
        # 'views/controllers_view.xml',
        'views/button_view.xml',
        'views/campus.xml',
        
        'views/student_exam_view.xml',
        'views/student_exam_schdule_view.xml',
        'views/student_leave_request_view.xml',
        'views/student_attendance_view.xml',
        'report/student_remider.xml',
        'report/email_student.xml',
        'report/student_final_report.xml',
        'report/TydAttendanceReport.xml',
        'report/student_attendance_report.xml',
        'report/all_classes.xml',
        'report/student_report.xml',
        'views/tyd_student_attendance.xml',
        'views/final_report_view.xml',
       
    ],
    
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    
}