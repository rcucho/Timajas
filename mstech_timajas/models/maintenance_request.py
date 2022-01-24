from odoo import models,fields,api,_
from datetime import timedelta, datetime
from odoo.exceptions import UserError

class MaintenanceRequestTimajas(models.Model):
    _inherit = "maintenance.request"
    
    mant_project = fields.Many2one('project.task', string="Proyecto")
    
    @api.onchange('stage_id')
    def _compute_mant_project(self):
        for record in self:
            if record.stage_id.id == 2:
                record.mant_project = self.env['project.task'].create({
                    'name': record.name,
                    'user_ids' : record.user_id,
                    'project_id' : 3,
                })

class MaintenanceEquipment2(models.Model):
    _inherit = "maintenance.equipment"
    
    eqip_product = fields.Many2one('product.product', string="Producto")
    #repuestos_proj = fields.One2many('stock.picking','move_ids_without_package', string="Repuestos Usados")
    
    @api.model
    def create(self, vals):
        equipment = super(MaintenanceEquipment2, self).create(vals)
        for record in equipment:
            record.eqip_product = self.env['product.product'].create({
                'name': record.name
            })
        return equipment
    
    #@api.onchange('maintenance_ids')
    #def _compute_mant_project(self):
        #for rec in self:
            #mov_pro = rec.maintenance_ids.mant_project.task_picking
            #/rec.repuestos_proj = rec.maintenance_ids.mant_project.task_picking.move_ids_without_package
            #for line in mov_pro:
                #rec.repuestos_proj = line.move_ids_without_package
    
class ProductTemplate(models.Model):
    _inherit = "product.product"
    
    product_eqip = fields.One2many('maintenance.equipment', 'eqip_product', string="Equipamento de Mantenimiento")
    project_count = fields.Integer(compute='_compute_project_count', string="Project Count", store= False)
    #
    project_pids = fields.Many2many('project.project', compute="_compute_project_ids", string='Projects')
    project_count2 = fields.Integer(compute='_compute_project_ids', string="Project Count")
    
    @api.depends('stock_move_ids')
    def _compute_project_count(self):
        for record in self:
            conta = len(record.stock_move_ids.filtered(lambda x: x.picking_id.picking_task))
            if conta % 2 == 0:
                record.project_count = conta/2
            else:
                record.project_count = (conta + 1)/ 2

    @api.depends('product_eqip')
    def _compute_project_ids(self):
        for rec in self:
            projects = rec.product_eqip.mapped('maintenance_ids.mant_project')
            #projects |= rec.order_line.mapped('project_id')
            #projects |= rec.project_id
            rec.project_pids = projects
            rec.project_count2 = len(projects)
                
                
class ProductTemplate(models.Model):
    _inherit = "product.template"
    
    #product_eqip_temp = fields.One2many('maintenance.equipment', 'eqip_product', string="Equipamento de Mantenimiento", compute='_compute_product_eqip_temp')
    product_eqip_temp = fields.One2many(string="Equipamento de Mantenimiento", related='product_variant_id.product_eqip')
    project_count_temp = fields.Integer(string="Project Count", related='product_variant_id.project_count')
    #@api.depends('name')
    #def _compute_product_eqip_temp(self):
        #for rec in self:
            #rec.product_eqip_temp = self.env['product.product'].browse(self._context['product_eqip'])
        
class ProjectTaskTimajas(models.Model):
    _inherit = "project.task"
    
    proj_mant = fields.One2many('maintenance.request','mant_project',string="Peticion de Mantenimiento")
    
