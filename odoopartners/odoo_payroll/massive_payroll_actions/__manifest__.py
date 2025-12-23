{
    'name': 'Massive payroll actions',
    'version': '17.0.1.1.0',
    'author': 'Ganemo',
    'website': 'https://www.ganemo.co',
    'description': """
Este modulo crea en el procesamiento masivo de nómina los botones Calcular nómina,confirmar y cambiar a borrador 
el cual facilita el calculo de una nómina varios trabajadores.
    """,
    'module_type': 'official',
    'depends': ['hr_payroll',
                'hr_payroll_account'],
    'data': ['views/hr_views.xml'],
    'installable': True,
    'auto_install': False,
    'license': 'Other proprietary',
    'currency': 'USD',
    'price': 0.00
}
