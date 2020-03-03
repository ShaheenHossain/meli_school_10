# -*- coding: utf-8 -*-
{
    'name': "afg_payroll",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "My Company",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/10.0/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','hr_contract','report_xlsx','hr_holidays','hr_attendance','hr_recruitment_survey','hr_expense','hr_public_holidays','mail','account'],

    # always loaded
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
        'wizards/payslip_batches_wizard.xml',
        'views/payslip_batches.xml',
        'views/excel_view.xml',
        'views/payslips_validation_approve.xml',
        'wizards/payslip_batch_pdf_wizard.xml',
        'reports/payslip_batch_pdf_report.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}