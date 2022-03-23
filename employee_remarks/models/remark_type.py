# -*- coding :utf-8 -*-

from openerp import models, fields


class RemarkType(models.Model):
    _name = "remark.type"
    _description = "Remark Type"

    name=fields.Char(string="Name",help="Name of the remark type",required=True)
    description=fields.Text(string="Description",help="description of the remark type")
