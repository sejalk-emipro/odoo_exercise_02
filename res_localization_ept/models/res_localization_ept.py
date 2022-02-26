# -*- coding :utf-8 -*-

from openerp import models,fields,api

class CountryData(models.Model):

    _name="res.country.ept"
    _description="Country Demo"

    name=fields.Char(string="Country Name",help="Name  of the country")
    code=fields.Char(string="Country Code",help="Short code of the country")
    state_ids=fields.One2many(comodel_name="res.state.ept",inverse_name="country_id",string="State",help="State")

    _sql_constraints=[
        ('unique_country_code','unique(code)','Add unique country code')
    ]

    @api.multi
    def check_crud_operation(self):
        states=self.state_ids.sudo().search([])
        # for s in states:
        #     print(s.name,s.code)
        countries=self.search([('code','in',['001','USA'])])
        print(countries[0])
        # new_record=self.env['res.country.ept'].create({'name':'India'})
        # print(new_record)
        is_write=self.write({'code':'IND1'})
        print(is_write)

    @api.model
    def create(self,vals):
        new_record=super(CountryData,self).create(vals)
        return new_record
    
    @api.model
    def write(self,vals):
        is_write=super(CountryData, self).write(vals)
        return is_write

