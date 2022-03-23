# -*- coding :utf-8 -*-

from openerp import models,fields

class HRJob(models.Model):
    _inherit="hr.job"

    hr_grace_hour_id=fields.Many2one(comodel_name="hr.grace.hour",string="Grace hours",help="Employee grace hours ref.")