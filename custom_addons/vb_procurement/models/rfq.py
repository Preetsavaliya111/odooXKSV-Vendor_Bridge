from odoo import models, fields

class RFQ(models.Model):
    _name = "vb.rfq"
    _description = "Request For Quotation"

    name = fields.Char(required=True)
    description = fields.Text()
    deadline = fields.Date()

    vendor_ids = fields.Many2many(
        "vb.vendor",
        string="Vendors"
    )

    quotation_ids = fields.One2many(
        "vb.quotation",
        "rfq_id",
        string="Quotations"
    )

    state = fields.Selection([
        ('draft', 'Draft'),
        ('sent', 'Sent'),
        ('closed', 'Closed')
    ], default='draft')