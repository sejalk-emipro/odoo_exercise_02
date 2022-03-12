from openerp import models,fields,api

class HRApplicant(models.Model):

    _name="hr.applicant"
    _inherit="hr.applicant"

    @api.multi
    def action_makeMeeting(self):
        """
            :functionality:- Smart button method. Inherited this method to set default values while creating a new calendar meeting.
            :return: Redict to calendar event view.
        """
        res=super(HRApplicant, self).action_makeMeeting()
        context=dict(res['context']) or {}
        type=self.env.ref('hr_employee_extended.meeting_type_prod_dem0')
        res['context']['default_categ_ids'].append(type.id)

        context.update({
            'default_class':'private',
            'default_show_as':'busy'
        })

        # res['context']['default_categ_ids'].append(type.id)
        # res['context']['default_class'] = "private"
        # res['context']['default_show_as'] = "busy"
        return res

