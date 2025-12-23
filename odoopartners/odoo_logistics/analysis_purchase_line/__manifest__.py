{
    'name': "Purchase Order Line Analysis",
    "category": "Purchases",
    "version": "17.0.1.0.1",
    "description": "Comprehensive tool for analyzing purchase orders and request for quotations (RFQs) at the line item level. Provides detailed insights and visualization options for enhanced procurement management.",
    "summary": "Analysis tool for purchase order lines and RFQs with multiple visualization options.",
    'author': 'Ganemo',
    'company': 'Ganemo',
    'website': "https://www.ganemo.co",
    'module_type': 'official',
    'depends': ['purchase'],
    'data': [
        "views/purchase_order_line_analysis.xml",
        'views/rfq_line_analysis.xml',
    ],
    'images': [
        'static/description/banner.png'
    ],
    'license': 'Other proprietary',
    'installable': True,
    'application': False,
    'auto_install': False,
    'currency': 'USD',
    'price': 97.00,
}

