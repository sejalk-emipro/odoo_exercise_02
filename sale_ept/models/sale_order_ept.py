# -*- coding :utf-8 -*-

from openerp import models,fields,api

class SaleOrderEPT(models.Model):
    _name="sale.order.ept"
    _description="Sale Order"

    name=fields.Char(string="Order No",help="Number of the order")
    partner_id=fields.Many2one(comodel_name="res.partner.ept",string="Customer",required=True,
                                domain="[('parent_id','=',False)]")
    partner_invoice_id=fields.Many2one(comodel_name="res.partner.ept",string="Invoice Customer",required=True,
                                       domain="[('address_type','=','Invoice'),('parent_id','=',partner_id)]")
    partner_shipping_id=fields.Many2one(comodel_name="res.partner.ept",string="Shipping Customer",required=True,
                                       domain="[('address_type','=','Shipping'),('parent_id','=',partner_id)]")
    sale_order_date=fields.Date(string="Sale Order Date",help="Date of the sale order",default=fields.Date.today())
    sale_person_id=fields.Many2one(comodel_name="res.users",string="Sales Person")
    state=fields.Selection([('Draft','Draft'),('Confirmed','Confirmed'),('Done','Done'),('Cancelled','Cancelled')],string="State",help="State of the order",default="Draft")

    order_line_ids=fields.One2many(comodel_name="sale.order.line.ept",inverse_name="order_id",string="Order line")
    total_weight=fields.Float(string="Total Weight", digits=(16,2), compute="compute_total_weight",store=False,help="Total of products weight of order")
    total_volume = fields.Float(string="Total Volume", digits=(16, 2), compute="compute_total_volume", store=False,help="Total of product volume of order")
    order_total=fields.Float(string="Order Total", digits=(16, 2), compute="compute_order_total", store=True,help="Total of the order")
    crm_lead_id=fields.Many2one(string="CRM Lead",comodel_name="crm.lead.ept")
    warehouse_id=fields.Many2one(string="Warehouse",comodel_name="stock.warehouse.ept")
    picking_ids=fields.One2many(comodel_name="stock.picking.ept",inverse_name="sale_order_id",
                                string="Pickings",readonly=True)
    picking_count=fields.Integer(string="Picking Count",compute="compute_count_picking", store=False)
    move_count = fields.Integer(string="Move Count", compute="compute_count_move", store=False)
    total_tax=fields.Float(string="Total Tax",compute="compute_total_tax",digits=(16,2),store=True)
    total_amount=fields.Float(string="Total Amount",compute="compute_total_amount",digits=(16,2),store=True)

    @api.depends('order_line_ids.subtotal_with_tax')
    def compute_total_amount(self):
        if self.order_line_ids:
            self.total_amount=sum(self.order_line_ids.mapped('subtotal_with_tax'))

    @api.depends('order_line_ids.subtotal_with_tax')
    def compute_total_tax(self):
        if self.order_line_ids:
            total_with_tax=sum(self.order_line_ids.mapped('subtotal_with_tax'))
            tota_without_tax=sum(self.order_line_ids.mapped('subtotal_without_tax'))
            self.total_tax=(total_with_tax-tota_without_tax)

    def compute_count_move(self):
        self.move_count = len(self.picking_ids.mapped('move_ids'))

    def compute_count_picking(self):
        self.picking_count=len(self.picking_ids)


    @api.multi
    def view_moves(self):
        # action = self.env['ir.actions.act_window'].for_xml_id('sale_ept', 'action_stock_moving')

        view=self.env.ref('sale_ept.view_stock_move_tree')
        action ={
            'name':'Stock Moves',
            'type':'ir.actions.act_window',
            'res_model':'stock.move.ept',
            'view_type': 'tree',
            'view_mode': 'tree',
            'views':[(False, 'tree')],
            'view_id': False,
            'target': 'current',
        }
        move_ids = self.picking_ids.mapped('move_ids').ids
        action['domain'] = "[('id','in',{0})]".format(move_ids)
        return action

    @api.multi
    def view_picking(self):
        '''
        This function returns an action that display existing picking orders of given sales order ids.
        '''

        action = self.env['ir.actions.act_window'].for_xml_id('sale_ept', 'action_delivery_orders')

        pick_ids =self.picking_ids.ids

        #choose the view_mode accordingly
        if len(pick_ids) > 1:
            action['domain'] = "[('id','in',{0})]".format(pick_ids)
        else:
            res =self.env['ir.ui.view'].for_xml_id('sale_ept', 'view_stock_picking_form')
            action['views'] = [(res and res[1] or False, 'form')]
            action['res_id'] = pick_ids and pick_ids[0] or False
        return action


    @api.multi
    def change_state_and_create_picking(self):
        """
        :functionality :Change the order state and create the Stock Picking on order
        :return: -
        """

        destination_location=self.env['stock.location.ept'].search([('location_type','=','Customer')],limit=1)
        if not destination_location:
            raise Warning("Customer cannot be found!.First add the customer in location")

        warehouses=self.order_line_ids.mapped('warehouse_id')

        if not warehouses:
            warehouses=[self.warehouse_id]

        for warehouse in warehouses:
            tmp_stock_moves = []
            order_line=self.order_line_ids.filtered(lambda line: line.warehouse_id.id == warehouse.id)

            if warehouse.id == self.warehouse_id.id:
                order_line=self.order_line_ids.filtered(lambda line: line.warehouse_id.id == warehouse.id or line.warehouse_id.id==False)

            for line in order_line:
                name='{0}: {1} -> {2}'.format(line.product_id.name,self.warehouse_id.stock_location_id.name,destination_location.name)
                tmp_stock_moves.append((0,0,{'sale_line_id':line.id,
                    'name':name,'product_id':line.product_id.id,
                    'uom_id':line.uom_id.id,
                    'source_location_id':warehouse.stock_location_id.id,
                    'destination_location_id':destination_location.id,
                    'qty_to_deliver':line.quantity,'qty_done':0.0}))
                line.write({'state':'Confirmed'})

            tmp_stock_picking=self.env['stock.picking.ept'].create({
            'partner_id':self.partner_shipping_id.id,
            'sale_order_id':self.id,
            'transaction_type':'Out',
            'move_ids':tmp_stock_moves})

        self.write({'state':'Confirmed'})

    @api.model
    def create(self, vals):
        vals['name'] = self.env['ir.sequence'].next_by_code('my.sale.order') or 'New'
        result = super(SaleOrderEPT, self).create(vals)
        return result

    @api.onchange('partner_id')
    def onchange_partner_id(self):
        if self.partner_id:
            # partners= self.env['res.partner.ept']
            # Using filter with lambda get invoice_partner and shipping partner
            invoice_partners=self.partner_id.child_ids.filtered(lambda partner: partner.address_type == 'Invoice' and partner.parent_id==self.partner_id)
            shipping_partner=self.partner_id.child_ids.filtered(lambda partner: partner.address_type == 'Shipping' and partner.parent_id==self.partner_id)

            # Using map with lambda get invoice_partner and shipping partner
            # mapped_invoice_partner=self.env['res.partner.ept'].search([('parent_id','=',self.partner_id.id),('address_type','=','Invoice')],limit=1).mapped('parent_id').child_ids
            # mapped_Shipping_partner = self.env['res.partner.ept'].search(
            #     [('parent_id', '=', self.partner_id.id), ('address_type', '=', 'Shipping')], limit=1).mapped('parent_id').child_ids

            # Using odoo search method get invoice_partner and shipping partner
            # invoice_partners1=partners.search([('parent_id','=',self.partner_id.id),('address_type','=','Invoice')],limit=1)
            # shipping_partner1=partners.search([('parent_id','=',self.partner_id.id),('address_type','=','Shipping')],limit=1)

            if not invoice_partners:
                self.partner_invoice_id=self.partner_id
            else:
                self.partner_invoice_id=invoice_partners[0]

            if not shipping_partner:
                self.partner_shipping_id=self.partner_id
            else:
                self.partner_shipping_id=shipping_partner[0]



    @api.depends('order_line_ids.subtotal_without_tax')
    def compute_order_total(self):
        for order in self:
            total=0
            for order_line in order.order_line_ids:
                total+=order_line.subtotal_without_tax
            order.order_total=total


    def compute_total_volume(self):
        for order in self:
            total_volume = 0
            for order_line in order.order_line_ids:
                total_volume += order_line.product_id.volume * order_line.quantity
            order.total_volume = total_volume

    def compute_total_weight(self):
        for order in self:
            total_weight=0
            for order_line in order.order_line_ids:
                total_weight+=order_line.product_id.weight * order_line.quantity
            order.total_weight=total_weight