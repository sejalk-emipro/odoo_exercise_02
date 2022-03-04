from openerp.osv import fields, osv
import openerp

class ir_sequence(openerp.osv.osv.osv):

    _inherit = 'ir.sequence'


    def _get_number_next_actual(self, cr, user, ids, field_name, arg, context=None):
        '''
            Override this method to fix increment by field error in sequence. it's due to
            latest version of postgres.
        '''
        res = dict.fromkeys(ids)
        for element in self.browse(cr, user, ids, context=context):
            if element.implementation != 'standard':
                res[element.id] = element.number_next
            else:
                # get number from postgres sequence. Cannot use
                # currval, because that might give an error when
                # not having used nextval before.
                statement = (
                        "SELECT last_value, is_called"
                        " FROM ir_sequence_%03d"
                        % element.id)
                cr.execute(statement)
                (last_value,is_called) = cr.fetchone()
                if is_called:
                    res[element.id] = last_value + 1
                else:
                    res[element.id] = last_value
        return res

    def _set_number_next_actual(self, cr, uid, id, name, value, args=None, context=None):
        return self.write(cr, uid, id, {'number_next': value or 0}, context=context)

    _columns = {
        'number_next_actual': openerp.osv.fields.function(_get_number_next_actual, fnct_inv=_set_number_next_actual,
                                                          type='integer', required=True, string='Next Number',
                                                          help='Next number that will be used. This number can be incremented frequently so the displayed value might already be obsolete'),
    }
