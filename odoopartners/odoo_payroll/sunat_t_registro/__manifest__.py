{
    'name': 'Sunat T-Registro',
    'version': '17.0.1.0.1',
    'author': 'Ganemo',
    'website': 'https://www.ganemo.co',
    'summary': 'This module outputs the files for bulk loading of the t-registro',
    'description': """
 This module facilitates the issuance of files necessary for mass upload to the T-Registry, complying with SUNAT specifications. 
 Designed to be compatible with both the community and enterprise versions of Odoo, the module integrates various functionalities that allow efficient management of employees and their associated records.
   It includes key dependencies such as hr, contacts, account, and more, ensuring broad coverage of operational needs.
     The files generated follow the structure required by SUNAT, including detailed fields for employee and successor data, such as start and end dates, document types, and contact information. 
     In addition, the module allows the generation of specific files for registrations and cancellations, as well as information updates, ensuring that all records are accurate and up-to-date. 
     The implementation is simple and it is recommended to test the community version to ensure its correct functioning.
""",
    'depends': [
        'account',
        'l10n_pe_edi',
        'hr',
        'personal_information',
        'eps_process',
        'payment_conditions',
        'employee_service',
        'types_system_pension',
        'various_data',
        'additional_fields_payroll',
        'identification_type_employee'
    ],
    'data': [
        'data/international.industrial.classification.csv',
        'data/ubigeo.reniec.object.csv',
        'data/occupational.worker.category.csv',
        'data/worker.type.pensioner.provider.csv',
        'data/type.formative.modality.work.csv',
        'data/occupation.work.personnel.training.modality.csv',
        'data/zone.type.object.csv',
        'data/road.type.object.csv',
        'data/edu.career.object.csv',
        'data/edu.name.object.csv',
        'data/edu.year.graduation.object.csv',
        'data/res_country.xml',
        'security/ir.model.access.csv',
        'wizards/hr_employee_relative_wizard.xml',
        'views/hr_contract_views.xml',
        'views/hr_employee_views.xml',
        'views/other_annexed_establishments_views.xml',
        'views/res_country_views.xml',
        'views/res_partner_views.xml',
        'views/sunat_t_registro_views.xml',
        'views/hr_employee_third_staff_views.xml',
        'views/third_staff_views.xml',
        'views/hr_employee_right_holders_views.xml',
        'views/hr_employee_relative_views.xml',
    ],
    'installable': True,
    'auto_install': False,
    'license': 'Other proprietary',
    'currency': 'USD',
    'price': 20.00,
    'module_type': 'official'
}
