from odoo import models, fields

class VendorCategory(models.Model):
    _name = "vb.vendor.category"
    _description = "Vendor Category"

    name = fields.Char(required=True)
    active = fields.Boolean(default=True)