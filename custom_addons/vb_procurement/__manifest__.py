# -*- coding: utf-8 -*-
{
    'name': 'VendorBridge Procurement ERP',

    'summary': 'Procurement and Vendor Management ERP',

    'description': """
VendorBridge Procurement ERP

Features:
- Vendor Management
- Vendor Categories
- RFQ Management
- Quotation Management
- Quotation Comparison
- Purchase Orders
- Invoice Generation
- Approval Workflow
- Procurement Analytics
""",

    'author': 'XKSV Team',
    'website': 'https://github.com/Preetsavaliya111/odooXKSV-Vendor_Bridge',

    'category': 'Purchases',
    'version': '1.0.0',

    'license': 'LGPL-3',

    'depends': ['base', 'mail'],

    'data': [
        'security/ir.model.access.csv',
        'data/sequence.xml',
        'reports/rfq_report.xml',
        'views/views.xml',
        'views/templates.xml',
        'security/groups.xml',
    ],  

    'demo': [],
}