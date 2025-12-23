{
    'name': 'Personal Information',
    'version': '17.0.1.1.0',
    'author': 'Ganemo',
    'website': 'https://www.ganemo.co',
    'category': 'Human Resources/Employees',
    'summary': 'Assignment of relatives to employees',
    'description': """
This module has been designed with the purpose of improving information management
personnel of employees by allowing the assignment of relatives.

In order to offer greater flexibility in data collection,
The module introduces four new fields in the employee file:

- Names
- Last name
- Mother's last name
- Relatives

In addition to adding these custom fields, the module hides three fields
natives of the employee record that will not be used:

- Spouse's full name (spouse_complete_name)
- Spouse's date of birth (spouse_birthdate)
- Number of dependent children (children)

Main Features:

- Assignment of relatives to employees.
- Additional fields: First names, Paternal last name, Maternal last name.
- Hiding native fields in the employee file that will not be used.
""",
    'depends': [
        'hr'
    ],
    'data': [
        'security/ir.model.access.csv',
        'data/hr_employee_relative_relation_data.xml',
        'views/hr_employee_relative_views.xml',
        'views/hr_employee_views.xml'
    ],
    'application': False,
    'installable': True,
    'auto_install': False,
    'license': 'Other proprietary',
    'currency': 'USD',
    'price': 20.00
}
