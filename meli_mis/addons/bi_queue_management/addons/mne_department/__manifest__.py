# -*- coding: utf-8 -*-
{
    'name': "mne_department",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "Karimi Infotech Pvt Ltd.",
    'website': "http://karimiinfotech.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/10.0/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','school','school_ems'],

    # always loaded
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/views.xml',
        'reports/audit_report.xml',
        'reports/student_complete_report.xml',
        'views/audit_view.xml',
        'views/student_feedback_view.xml',
        'views/complete_survey_view_form.xml',

        'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}