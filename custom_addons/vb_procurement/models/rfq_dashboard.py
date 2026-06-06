from odoo import models, fields


class RFQDashboard(models.Model):
    _name = "vb.rfq.dashboard"
    _description = "RFQ Dashboard"

    total_rfqs = fields.Integer()
    draft_rfqs = fields.Integer()
    sent_rfqs = fields.Integer()
    approved_rfqs = fields.Integer()
    rejected_rfqs = fields.Integer()
    closed_rfqs = fields.Integer()

    def get_dashboard_data(self):
        rfq = self.env['vb.rfq']

        return {
            'total_rfqs': rfq.search_count([]),
            'draft_rfqs': rfq.search_count([('state', '=', 'draft')]),
            'sent_rfqs': rfq.search_count([('state', '=', 'sent')]),
            'approved_rfqs': rfq.search_count([('state', '=', 'approved')]),
            'rejected_rfqs': rfq.search_count([('state', '=', 'rejected')]),
            'closed_rfqs': rfq.search_count([('state', '=', 'closed')]),
        }