# -*- coding: utf-8 -*-
from odoo import fields, models, api, _
from odoo.exceptions import ValidationError


class UtilsResPartner(models.Model):
    _name = 'res.partner.utils'

    @api.onchange('parent_id')
    def _onchange_service(self):
        domain = {'child_ids': []}
        for rec in self:
            if rec.parent_id:
                domain = {'child_ids': [('parent_id', '=', rec.parent_id.id)]}
        return {'domain': domain}

    name = fields.Char(string='Nombre del servicio', required=True)
    parent_id = fields.Many2one('res.partner.utils', string='Categoria de Servicios', index=True, ondelete='cascade')
    child_ids = fields.One2many('res.partner.utils', 'parent_id', string='Servicios')
    activo = fields.Boolean(default=True)

    partner_ids = fields.Many2many('res.partner.servicios', column1='servs_id', column2='partner_id',
                                    string='Pacientes', domain=_onchange_service)

    # subpartner_ids = fields.Many2many('res.partner.servicios', column1='subservs_id', column2='partner_id',
    #                                string='Pacientes')

    @api.constrains('parent_id')
    def _check_parent_id(self):
        if not self._check_recursion():
            raise ValidationError(_('No puedes crear servicios recursivos.'))


class UtilsResService(models.Model):
    _name = 'res.service.utils'

    tratamientos_id = fields.Many2one('res.partner.servicios')
    fecha = fields.Date('Fecha')
    servicio = fields.Selection([('T', 'Tratamiento'), ('P', 'Producto')], string='Servicio/Producto')
    detalle = fields.Text('Detalle')