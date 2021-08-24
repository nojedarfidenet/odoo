# -*- coding: utf-8 -*-
from datetime import datetime

from odoo import fields, models


class IrAttachments(models.Model):
    _inherit = "ir.attachment"

    fecha = fields.Date('Fecha', default=datetime.today().date())
    partner_id = fields.Many2one('res.partner')
    adjunto_id = fields.Many2one('res.partner.servicios')
