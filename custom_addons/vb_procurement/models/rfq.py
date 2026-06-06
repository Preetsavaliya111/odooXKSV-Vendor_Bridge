from odoo import models, fields, api
from odoo.exceptions import ValidationError


class RFQ(models.Model):
    _name = "vb.rfq"
    _description = "Request For Quotation"

    # =========================
    # BASIC INFO
    # =========================
    name = fields.Char(required=True)
    description = fields.Text()
    deadline = fields.Date()

    state = fields.Selection([
        ('draft', 'Draft'),
        ('sent', 'Sent'),
        ('quoted', 'Quoted'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('closed', 'Closed')
    ], default='draft')

    # =========================
    # RELATIONS
    # =========================
    vendor_ids = fields.Many2many("vb.vendor", string="Vendors")

    quotation_ids = fields.One2many(
        "vb.quotation",
        "rfq_id",
        string="Quotations"
    )

    best_quotation_id = fields.Many2one(
        "vb.quotation",
        compute="_compute_best_quote",
        store=True
    )

    best_vendor_id = fields.Many2one(
        "vb.vendor",
        compute="_compute_best_quote",
        store=True
    )

    # =========================
    # VALIDATIONS
    # =========================
    @api.constrains('name')
    def _check_name(self):
        for rec in self:
            if not rec.name or len(rec.name.strip()) < 3:
                raise ValidationError("RFQ name must be at least 3 characters long.")

    @api.constrains('vendor_ids')
    def _check_vendors(self):
        for rec in self:
            if not rec.vendor_ids:
                raise ValidationError("Please select at least one vendor.")

    @api.constrains('deadline')
    def _check_deadline(self):
        for rec in self:
            if rec.deadline and rec.deadline < fields.Date.today():
                raise ValidationError("Deadline cannot be in the past.")

    # =========================
    # BEST QUOTE ENGINE
    # =========================
    @api.depends(
        'quotation_ids.price',
        'quotation_ids.delivery_days',
        'quotation_ids.state',
        'state'
    )
    def _compute_best_quote(self):
        for rfq in self:

            if rfq.state in ('closed', 'rejected'):
                rfq.best_quotation_id = False
                rfq.best_vendor_id = False
                continue

            best_quote = False
            best_score = float('inf')

            for q in rfq.quotation_ids:
                if q.state not in ('submitted', 'accepted'):
                    continue

                price = q.price or 0.0
                delivery = q.delivery_days or 0.0

                score = (price * 0.7) + (delivery * 0.3)

                if score < best_score:
                    best_score = score
                    best_quote = q

            rfq.best_quotation_id = best_quote
            rfq.best_vendor_id = best_quote.vendor_id if best_quote else False

    # =========================
    # ACTION 1: SEND RFQ (SAFE)
    # =========================
    def action_send_to_vendors(self):
        for rfq in self:
            template = self.env.ref('mail.template_data_warning', raise_if_not_found=False)

            for vendor in rfq.vendor_ids:
                if vendor.email:
                    self.env['mail.mail'].sudo().create({
                        'subject': f'RFQ Invitation: {rfq.name}',
                        'body_html': f"""
                            <p>Hello {vendor.name},</p>
                            <p>You are invited to submit a quotation for RFQ <b>{rfq.name}</b>.</p>
                            <p>Deadline: {rfq.deadline}</p>
                        """,
                        'email_to': vendor.email,
                    }).send()

            rfq.state = 'sent'

    # =========================
    # ACTION 2: COMPUTE
    # =========================
    def action_compute_best_quote(self):
        for rfq in self:
            if not rfq.quotation_ids:
                continue

            def score(q):
                price_score = q.price
                delivery_score = q.delivery_days or 999

                # weighted scoring (lower is better)
                return (price_score * 0.7) + (delivery_score * 0.3)

            best = min(rfq.quotation_ids, key=score)

            rfq.best_vendor_id = best.vendor_id.id

            for q in rfq.quotation_ids:
                q.is_best_price = (q.id == best.id)

            rfq.state = 'computed'

    # =========================
    # ACTION 3: APPROVE
    # =========================
    def action_approve_rfq(self):
        for rfq in self:
            if not rfq.best_quotation_id:
                raise ValidationError("Cannot approve RFQ without a valid quotation.")

            rfq.state = 'approved'

    # =========================
    # ACTION 4: REJECT
    # =========================
    def action_reject_rfq(self):
        for rfq in self:
            rfq.state = 'rejected'

    # =========================
    # ACTION 5: CREATE PO
    # =========================
    def action_create_purchase_order(self):
        PurchaseOrder = self.env['vb.purchase.order']

        for rfq in self:

            if not rfq.best_quotation_id:
                raise ValidationError("No best quotation found.")

            quote = rfq.best_quotation_id

            po = PurchaseOrder.create({
                'name': self.env['ir.sequence'].next_by_code('vb.po') or f"PO/{rfq.name}",
                'quotation_id': quote.id,
                'vendor_id': quote.vendor_id.id,
                'amount': quote.price,
                'state': 'draft'
            })

            rfq.state = 'closed'

            return {
                'type': 'ir.actions.act_window',
                'res_model': 'vb.purchase.order',
                'view_mode': 'form',
                'res_id': po.id,
                'target': 'current',
            }

    # =========================
    # ACTION 6: PRINT RFQ
    # =========================
    def action_print_rfq(self):
        return self.env.ref('vb_procurement.action_report_rfq').report_action(self)