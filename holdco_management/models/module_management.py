from odoo import models, fields, api

class HoldcoModuleManagement(models.Model):
    _name = 'holdco.module.management'
    _description = 'Module Management'

    name = fields.Char(string="Name", required=True)
    version = fields.Char(string="Version")
    state = fields.Selection([
        ('not_installed', 'Not Installed'),
        ('installed', 'Installed'),
    ], string="State", default='not_installed')
    
    install = fields.Boolean(string="Install")

    @api.onchange('install')
    def _onchange_install(self):
        if self.install:
            self.state = 'installed'
        else:
            self.state = 'not_installed'

    @api.model
    def create(self, vals):
        record = super(HoldcoModuleManagement, self).create(vals)
        if vals.get('install'):
            record.install_module()
        else:
            record.uninstall_module()
        return record

    def write(self, vals):
        res = super(HoldcoModuleManagement, self).write(vals)
        if 'install' in vals:
            if vals['install']:
                self.install_module()
            else:
                self.uninstall_module()
        return res

    def install_module(self):
        # Lógica para instalar el módulo
        self.state = 'installed'

    def uninstall_module(self):
        # Lógica para desinstalar el módulo
        self.state = 'not_installed'
