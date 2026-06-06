from odoo import models, fields, api


class PurchaseOrder(models.Model):
    _name = "vb.purchase.order"
    _description = "Purchase Order"

    name = fields.Char(
        string="PO Number",
        required=True,
        copy=False,
        default="New"
    )

    quotation_id = fields.Many2one(
        "vb.quotation",
        string="Quotation",
        required=True
    )

    vendor_id = fields.Many2one(
        "vb.vendor",
        string="Vendor",
        related="quotation_id.vendor_id",
        store=True
    )

    amount = fields.Float(
        related="quotation_id.price",
        store=True
    )

    state = fields.Selection([
        ("draft", "Draft"),
        ("confirmed", "Confirmed")
    ], default="draft")

    @api.model
    def create(self, vals):
        if vals.get("name", "New") == "New":
            vals["name"] = self.env["ir.sequence"].next_by_code(
                "vb.purchase.order"
            ) or "New"

        return super().create(vals)