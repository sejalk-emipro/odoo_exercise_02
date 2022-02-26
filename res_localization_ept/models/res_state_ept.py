# -*- coding :utf-8 -*-

from openerp import models,fields,api

class StateData(models.Model):

    _name="res.state.ept"
    _description="State Demo"

    name=fields.Char(string="State Name",help="Name of the state")
    code=fields.Char(string="State Code",help="Code of the state")
    country_id=fields.Many2one(comodel_name="res.country.ept",string="Country",help="Name of The Country",copy=False)
    city_ids=fields.One2many(comodel_name="res.city.ept",inverse_name="state_id",string="City",help="Name of the City")

    # def copy(self,cr, uid, ids, default=None, context=None):
    #     if not default:
    #         default = {}
    #     default['name']=self.name + "- Copy"
    #     new_record=super(StateData, self).copy(cr, uid, ids,default=default,context=context)
    #     return new_record

    @api.multi
    def copy(self, default={}):
        default.update({
            'name': self.name+" - Copy"
        })
        new_record =super(StateData, self).copy(default)
        return new_record

    @api.constrains('code')
    def check_unique_code(self):
        if self.search([('code', '=ilike', self.code), ('id', '!=', self.id)],limit=1):
            raise Warning("State code cannot be duplicate")

