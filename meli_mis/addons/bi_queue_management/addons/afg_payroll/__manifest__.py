# -*- coding: utf-8 -*-
{
    'name': "afg_payroll",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "Karimi InfoTech Pvt Ltd.",
    'website': "http://www.karimiinfotech.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/10.0/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','l10n_in_hr_payroll','hr_contract','report_xlsx','hr_payroll','hr_holidays','hr_attendance','sale_timesheet','hr_recruitment','hr_recruitment_survey','hr_expense','school','resource','bi_mustroll_excel','bi_sqlconnector','dev_employee_profile','hr_public_holidays','oh_employee_documents_expiry','mail','hr_payroll_account'],

    # always loaded
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
        'views/payslip_batches.xml',
        'wizards/payslip_batches_wizard.xml',
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