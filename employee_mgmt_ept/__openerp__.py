# -*- coding :utf-8 -*-
{
    'name':'Employee Management',
    'category':'Utility',
    'version':'1.1',
    'author':'Emipro Technology Pvt. Ltd.',
    'description':"""
    This module for the demonstration of the student info
    """,
    'website':'https://www.emiprotechnologies.com',
    'depends':['sales_team'],
    'data':['security/employee_mgmt_security.xml',
            'security/ir.model.access.csv',
            'views/employee_ept.xml',
            'views/employee_dept_shift.xml',
            'views/employee_department.xml',
            'views/employee_leave_ept.xml'],
    'demo':[],
    'sequence':17,
    'auto_install':False,
    'application':False,
    'installable':True
}