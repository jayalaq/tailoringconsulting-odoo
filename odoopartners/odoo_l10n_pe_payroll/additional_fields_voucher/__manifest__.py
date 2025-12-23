{
    'name': 'Additional fields voucher',
    'version': '17.0.1.1.2',
    'author': 'Ganemo', 
    'website': 'https://www.ganemo.co',
    'category': 'Payroll', 
    'summary': 'this module adds the employee signature field in the HR configuration tab',
    'description': """
Este módulo debe funcionar en enterprise y comunitario, por lo que se recomienda testear con comunitario.
Las dependencias son referenciales. Si en el desarrollo se detecta que son necesarias más o menos dependencias, agregarlas.
""",
    'depends': [
        'hr_payroll',
        'identification_type_employee'
    ],
    'data': ['views/hr_views.xml'],
    'installable': True,
    'auto_install': False,
    'license': 'Other proprietary',
    'currency': 'USD',
    'price': 20.00,
    'module_type': 'official'
}
