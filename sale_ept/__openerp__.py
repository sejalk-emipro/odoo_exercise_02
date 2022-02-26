#-*- coding :utf-8 -*-

{
    'name':'sale_ept',
    'category':'Utility',
    'author':'Emipro technology pvt. ltd.',
    'version':'1.1',
    'website':'https://www.emiprotechnologies.com',
    'description':"""
    This module for the demonstration of the sales data
    """,
    'depends':['sales_team','res_localization_ept'],
    'data':['security/ir.model.access.csv',
            'views/product_category_ept.xml',
            'views/product_ept.xml',
            'views/product_uom_category_ept.xml',
            'views/product_uom_ept.xml',
            'views/res_partner_ept.xml',
            'views/sales_order_ept.xml',
            'views/sale_order_line_ept.xml'],
    'demo':[],
    'auto_install':False,
    'application':False,
    'installable':True,
}