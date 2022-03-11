#-*- coding :utf-8 -*-

{
    'name':'Sale Ept',
    'category':'Utility',
    'author':'Emipro technology pvt. ltd.',
    'version':'1.1',
    'website':'https://www.emiprotechnologies.com',
    'description':"""
    This module for the demonstration of the sales data
    """,
    'depends':['sales_team','res_localization_ept'],
    'data':['security/ir.model.access.csv',
            'data/sale_sequence.xml',
            'data/picking_sequence.xml',
            'data/purchase_sequence.xml',
            'views/product_category_ept.xml',
            'views/product_ept.xml',
            'views/product_uom_category_ept.xml',
            'views/product_uom_ept.xml',
            'views/res_partner_ept.xml',
            'views/sales_order_ept.xml',
            'views/sale_order_line_ept.xml',
            'views/crm_team_ept.xml',
            'views/crm_lead_ept.xml',
            'views/stock_location_ept.xml',
            'views/stock_warehouse_ept.xml',
            'views/stock_picking_ept.xml',
            'views/purchase_order_ept.xml',
            'views/purchase_order_line_ept.xml',
            'views/stock_inventory_ept.xml',
            'wizard/product_stock_update_ept.xml',
            'views/account_tax_ept.xml'],
    'demo':[],
    'auto_install':False,
    'application':False,
    'installable':True,
}