# -*- coding :utf-8 -*-

from openerp import models,fields,api
from openerp.exceptions import Warning

class HRGraceHourSlots(models.Model):
    _name="hr.grace.hour.slots"
    _description="HR Grace Slots"

    name=fields.Char(string="Name",required=True,help="Name of the grace hour slot")
    slot=fields.Integer(string="Slot",required=True,help="Duration of the slot")
    no_of_leave_days=fields.Float(string="No. of Leave Days",digits=(6,2),help="Count of the leave days")
    sequence=fields.Integer(string="Sequence")
    grace_hour_id=fields.Many2one(comodel_name="hr.grace.hour",string="Grace Hour")


    @api.constrains('sequence')
    def check_unique_sequence(self):
        """
        :functionality : check unique sequence constrains of the Grace Hours Slots
        :return: -
        """
        if self.sequence <= 0:
            raise Warning("Slot sequence must be Positive and non Zero.")
        if self.search([('sequence', '=', self.sequence),('grace_hour_id','=',self.grace_hour_id.id), ('id', '!=', self.id)], limit=1):
            raise Warning("Slot sequence cannot be duplicate")