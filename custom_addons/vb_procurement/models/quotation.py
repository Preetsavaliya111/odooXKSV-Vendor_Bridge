from odoo import models, fields, api


class VendorQuotation(models.Model):
    _name = "vb.quotation"
    _description = "Vendor Quotation"
    _rec_name = "display_name"

    # =====================================================
    # RELATIONS
    # =====================================================
    rfq_id = fields.Many2one(
        "vb.rfq",
        string="RFQ",
        required=True,
        ondelete="cascade"
    )

    vendor_id = fields.Many2one(
        "vb.vendor",
        string="Vendor",
        required=True
    )

    # =====================================================
    # QUOTATION DETAILS
    # =====================================================
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

    # =====================================================
    # DISPLAY NAME (FIXED SAFE COMPUTE)
    # =====================================================
    display_name = fields.Char(
        compute="_compute_display_name",
        store=False
    )

    @api.depends('vendor_id', 'price')
    def _compute_display_name(self):
        for rec in self:
            vendor = rec.vendor_id.name or "Vendor"
            price = rec.price or 0.0

            rec.display_name = f"{vendor} - ₹{price:,.0f}"

    # =====================================================
    # ACTIONS (OPTIONAL BUT IMPORTANT FOR FLOW)
    # =====================================================
    def action_submit(self):
        for rec in self:
            rec.state = 'submitted'

    def action_accept(self):
        for rec in self:
            rec.state = 'accepted'

    def action_reject(self):
        for rec in self:
            rec.state = 'rejected'