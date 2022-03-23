# -*- coding :utf-8 -*-
{
    'name':'HR Grace Slots',
    'category':'Utility',
    'version':'1.1',
    'author':'Emipro Technology Pvt. Ltd.',
    'description':"""
    This module for the demonstration of the grace slots
    """,
    'website':'https://www.emiprotechnologies.com',
    'depends':['hr_evaluation',],
    'data':['security/ir.model.access.csv',
            'views/hr_job.xml',
            'data/ir_cron.xml',
            'views/hr_grace_hour.xml',
            'views/hr_employee_grace_hours.xml',],
    'demo':[],
    'sequence':16,
    'auto_install':False,
    'application':False,
    'installable':True
}