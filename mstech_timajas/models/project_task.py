from odoo import models,fields,api,_
from datetime import timedelta, datetime
from odoo.exceptions import UserError

class ProjectTaskTimajas(models.Model):
    _inherit = "project.task"
    
    create_function = fields.Char(related='create_uid.function', readonly=True)
    state_payment_invoice = fields.Selection(related='sale_order_id.invoice_ids.payment_state',string="Estado de Pago Factura" ,readonly=True)  
    #---------------------------------------------------------------------------------------------
    task_picking = fields.One2many('stock.picking','picking_task', string="Herram.")
    equipos_mantenimiento = fields.Html(string='Equipos para Mantenimiento')
    om_mrp = fields.One2many('mrp.production','om_project',string="Ordenn de Manufactura") 
    #---------------------------------------------------------------------------------------------
class MrpProducction(models.Model):
    _inherit = "mrp.production"
    om_project = fields.Many2one('project.task', string="OM en Proyecto")
    
    @api.onchange('om_project', 'product_id')
    def onchange_origin_location(self):
        for record in self:
            if record.om_project:
                record.origin = record.om_project.sale_order_id.name
                record.location_src_id = (20, 'EW/Stock')
                record.location_dest_id = (20, 'EW/Stock')
    
class StockPickingTask(models.Model):
    _inherit = 'stock.picking'   
    picking_task = fields.Many2one('project.task', string="tarea en movimiento")
    
    @api.model
    def create(self, vals):
        defaults = self.default_get(['name', 'picking_type_id'])
        picking_type = self.env['stock.picking.type'].browse(vals.get('picking_type_id', defaults.get('picking_type_id')))             
        if self.picking_task:
            if vals.get('name', '/') == '/' and defaults.get('name', '/') == '/' and vals.get('picking_type_id', defaults.get('picking_type_id')):
                vals['name'] = picking_type.sequence_id.next_by_id()
        res = super(StockPickingTask,self).create(vals)      
        return res
    
    @api.onchange('picking_type_id', 'partner_id')
    def onchange_picking_type(self):
        for record in self:
            if record.picking_task:
                record.picking_type_id = (5, 'San Francisco: Internal Transfers')
        #picki = super().onchange_picking_type()
        #return picki
    
    @api.onchange('partner_id')
    def onchange_partner_id(self):
        for record in self:
            if record.picking_task:
                record.partner_id = record.picking_task.partner_id
        #parti = super().onchange_partner_id()
        parti = None
        if hasattr(super(), 'onchange_partner_id'):
            parti = super().onchange_partner_id()
        return parti
    
    @api.depends('state', 'move_lines', 'move_lines.state', 'move_lines.package_level_id', 'move_lines.move_line_ids.package_level_id')
    def _compute_move_without_package(self):
        for record in self:
            if record.picking_task:
                movimi = record.move_ids_without_package
                #herra = movimi.filtered(lambda x_h: x_h.product_id.categ_id.name == 'Herramientas')
                #record.move_ids_without_package = herra        
                pass
        mov_he = super()._compute_move_without_package()
        return mov_he
    
    def validate_directo(self):
        for record in self:
            record.action_confirm()
            record.action_assign()
            if record.action_assign() == True:
                record.button_validate()
                #record.button_validate()
        return True
