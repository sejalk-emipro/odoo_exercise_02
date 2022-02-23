# -*- coding :utf-8 -*-

from openerp import models,fields

class StudentInfo(models.Model):

    _name="student.ept"
    _description="student info"

    name=fields.Char(string="Student Name",help="Name of the student.", required=True)
    stud_class=fields.Char(string="Student Class",help="Class of the student.",required=True)
    dob=fields.Date(string="Birth Date",help="Birth date of the student",required=True)
    courses_ids=fields.Many2many(comodel_name="course.ept",string="Course",help="Enter course of the student")
