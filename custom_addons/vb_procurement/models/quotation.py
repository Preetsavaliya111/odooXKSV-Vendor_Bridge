from odoo import models, fields

class VendorQuotation(models.Model):
    _name = "vb.quotation"
    _description = "Vendor Quotation"

    rfq_id = fields.Many2one(
        "vb.rfq",
        string="RFQ",
        required=True
    )

    vendor_id = fields.Many2one(
        "vb.vendor",
        string="Vendor",
        required=True
    )

    price = fields.Float(required=True)

    delivery_days = fields.Integer()

    notes = fields.Text()

    is_best_price = fields.Boolean(
        string="Best Price",
        default=False
    )

    state = fields.Selection([
        ('draft', 'Draft'),
        ('submitted', 'Submitted'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected')
    ], default='draft')