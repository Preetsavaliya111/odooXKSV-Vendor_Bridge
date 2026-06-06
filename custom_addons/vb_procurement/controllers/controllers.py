# -*- coding: utf-8 -*-
# from odoo import http


# class VbProcurement(http.Controller):
#     @http.route('/vb_procurement/vb_procurement', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/vb_procurement/vb_procurement/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('vb_procurement.listing', {
#             'root': '/vb_procurement/vb_procurement',
#             'objects': http.request.env['vb_procurement.vb_procurement'].search([]),
#         })

#     @http.route('/vb_procurement/vb_procurement/objects/<model("vb_procurement.vb_procurement"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('vb_procurement.object', {
#             'object': obj
#         })

