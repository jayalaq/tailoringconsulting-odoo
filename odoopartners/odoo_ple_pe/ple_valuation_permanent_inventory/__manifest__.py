{
    'name': 'Libro kardex valorizado PLE - SUNAT (Perú)',
    'version': '17.0.1.0.1',
    'author': 'Ganemo',
    'website': 'https://www.ganemo.co',
    'category': 'Accounting',
    'summary': 'Valuated permanent inventory record (Valued kardex)',
    'description':"""
It issues the valued permanent inventory book that is mandatory for Peruvian companies that invoice above 1500 UIT. You can generate the .txt file to directly present through the electronic book program (PLE-SUNAT).
""",
    'depends': [
        'ple_permanent_inventory_in_physical_units',
    ],
    'data': [
        'views/ple_permanent_inventory_physical_units_views.xml',
    ],
    'application':False,
    'installable': True,
    'auto_install': False,
    'license': 'Other proprietary',
    'currency': 'USD',
    'price': 399.00,
    'module_type': 'official',
}