from odoo import models, fields

class VbDashboard(models.Model):
    _name = "vb.dashboard"
    _description = "VendorBridge Dashboard"

    total_rfq = fields.Integer(compute="_compute")
    approved_rfq = fields.Integer(compute="_compute")
    pending_rfq = fields.Integer(compute="_compute")
    total_vendors = fields.Integer(compute="_compute")

    def _compute(self):
        rfq = self.env['vb.rfq']
        vendor = self.env['vb.vendor']

        for rec in self:
            rec.total_rfq = rfq.search_count([])
            rec.approved_rfq = rfq.search_count([('state', '=', 'approved')])
            rec.pending_rfq = rfq.search_count([('state', '!=', 'approved')])
            rec.total_vendors = vendor.search_count([])