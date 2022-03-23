#-*- coding :utf-8 -*-

from openerp import models,fields

class EmployeeResConfig(models.TransientModel):
    _inherit = 'hr.config.settings'

    default_marital= fields.Selection([('single', 'Single'), ('married', 'Married'),('widower', 'Widower'), ('divorced', 'Divorced')]
         , 'Default Marital Status', type='selection',default_model='hr.employee')

    _defaults = {
        'default_marital': 'single',
    }