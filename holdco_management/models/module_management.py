
from odoo import models, fields, api

class ModuleManagement(models.Model):
    _name = 'holdco.module.management'
    _description = 'Module Management'

    name = fields.Char(string='Module Name', required=True)
    version = fields.Char(string='Version', compute='_compute_version')
    state = fields.Selection([
        ('not_installed', 'Not Installed'),
        ('installed', 'Installed'),
    ], string='State', default='not_installed')

    @api.depends('name')
    def _compute_version(self):
        for record in self:
            module = self.env['ir.module.module'].search([('name', '=', record.name)], limit=1)
            record.version = module.latest_version if module else 'N/A'

    def install_module(self):
        for record in self:
            module = self.env['ir.module.module'].search([('name', '=', record.name)])
            if module and module.state == 'uninstalled':
                module.button_immediate_install()
                record.state = 'installed'

    def uninstall_module(self):
        for record in self:
            module = self.env['ir.module.module'].search([('name', '=', record.name)])
            if module and module.state == 'installed':
                module.button_immediate_uninstall()
                record.state = 'not_installed'
