from odoo import models, fields


class Vendor(models.Model):
    _name = "vb.vendor"
    _description = "Vendor"

    name = fields.Char(required=True)
    email = fields.Char()
    gst_number = fields.Char()
    active = fields.Boolean(default=True)
    category_id = fields.Many2one(
    "vb.vendor.category",
    string="Category"
)