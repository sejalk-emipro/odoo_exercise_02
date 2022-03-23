# -*- coding :utf-8 -*-
{
    'name':'Employee Remarks',
    'category':'Utility',
    'version':'1.1',
    'author':'Emipro Technology Pvt. Ltd.',
    'description':"""
    This module for the demonstration of the employee remarks
    """,
    'website':'https://www.emiprotechnologies.com',
    'depends':['hr_evaluation'],
    'data':['security/employee_remark_security.xml',
            'security/ir.model.access.csv',
            'data/employee_remarks_sequence.xml',
            'data/employee_notify_remark.xml',
            'wizard/employee_comment.xml',
            'wizard/improvement_remark.xml',
            'wizard/notify_to_employee.xml',
            'views/remark_type.xml',
            'views/employee_remarks.xml',
            'views/employee_comments.xml',
            'views/improvement_remarks.xml',
            'report/employee_remark_report.xml',
            'report/report_employee_remark.xml',
            ],
    'demo':[],
    'sequence':16,
    'auto_install':False,
    'application':False,
    'installable':True
}