# -*- coding :utf-8 -*-

from openerp import models,fields

class HRGraceHour(models.Model):
    _name="hr.grace.hour"
    _description="HR Grace Hour"

    name=fields.Char(string="Name",help="Name of the grace hour",required=True)
    active=fields.Boolean(string="Active",required=True,default=True)
    slot_ids=fields.One2many(comodel_name="hr.grace.hour.slots",inverse_name="grace_hour_id",string="Grace Slot")