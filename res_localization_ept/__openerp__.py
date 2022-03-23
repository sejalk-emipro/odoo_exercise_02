# -*- coding :utf-8 -*-
{
    'name':'Localization',
    'category':'Utility',
    'version':'1.1',
    'author':'Emipro Technology Pvt. Ltd.',
    'description':"""
    This module for the demonstration of the country data
    """,
    'website':'https://www.emiprotechnologies.com',
    'depends':['sales_team'],
    'data':['security/ir.model.access.csv',
            'views/res_country_ept.xml',
            'views/res_state_ept.xml',
            'views/res_city_ept .xml',
            'report/country_report.xml',
            'report/country_report_template.xml',],
    'demo':[],
    'sequence':15,
    'auto_install':False,
    'application':False,
    'installable':True
}