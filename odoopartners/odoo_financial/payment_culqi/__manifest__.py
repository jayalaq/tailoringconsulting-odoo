{
    "name": "Culqi Payment Acquirer",
    "version": "17.0.1.0.3",
    "author": "Ganemo",
    "website": "https://www.ganemo.co",
    "summary": "Accounts receivable and payable reports with cut-off date and aging reports.",
    "description": """
Incorporating the Culqi payment method allows easy integration 
with this widely used Peruvian payment method.    
    """,
    "category": "eCommerce",
    "depends": ["payment"],
    "data": [
        "views/payment_provider_views.xml",
        "views/payment_culqi_templates.xml",
        "data/payment_provider_data.xml",
    ],
    "assets": {
        "web.assets_frontend": [
            "payment_culqi/static/src/js/payment_form.js",
        ],
    },
    "application": False,
    "installable": True,
    "auto_install": False,
    "module_type": "official",
    "license": "Other proprietary",
    "post_init_hook": "post_init_hook",
    "uninstall_hook": "uninstall_hook",
    "currency": "USD",
    "price": 100.00,
}
