# -*- coding :utf-8 -*-

from openerp import models,fields

class Course(models.Model):

    _name="course.ept"
    _description="Course Data"

    name=fields.Char(string="Course Name",help="Name of the course",required=True)
    student_ids=fields.Many2many(comodel_name="student.ept",string="Student",help="")