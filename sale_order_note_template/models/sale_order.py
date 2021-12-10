
from odoo import api, fields, models


class SaleOrder(models.Model):

    _inherit = "sale.order"

    terms_template_id_head = fields.Many2one(
        "sale.terms_template",
        string="Text Header",
        readonly=True,
        states={"draft": [("readonly", False)]},
    )
    terms_template_id_block = fields.Many2one(
        "sale.terms_template",
        string="Block Text",
        readonly=True,
        states={"draft": [("readonly", False)]},
    )
    terms_template_id_terms = fields.Many2one(
        "sale.terms_template",
        string="Terms and conditions",
        readonly=True,
        states={"draft": [("readonly", False)]},
    )
    terms = fields.Html(string="Text Terms", readonly=True, states={"draft": [("readonly", False)]})
    head = fields.Html(string="Text Header", readonly=True, states={"draft": [("readonly", False)]})
    block = fields.Html(string="Block Text", readonly=True, states={"draft": [("readonly", False)]})

    @api.onchange("terms_template_id_terms")
    def _onchange_terms_template_id(self):
        if self.terms_template_id_terms:
            self.terms = self.terms_template_id_terms.get_value(self)
        
    @api.onchange("terms_template_id_block")
    def _onchange_block_template_id(self):
        if self.terms_template_id_block:
            self.block = self.terms_template_id_block.get_value(self)

    @api.onchange("terms_template_id_head")
    def _onchange_head_template_id(self):
        if self.terms_template_id_head:
            self.head = self.terms_template_id_head.get_value(self)
            

    