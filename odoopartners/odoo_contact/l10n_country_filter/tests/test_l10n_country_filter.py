from lxml import etree
from odoo.tests import tagged
from odoo.tests.common import TransactionCase


@tagged('l10n_country_filter', 'post_install', '-at_install', '-standard')
class TestL10nCountryFilter(TransactionCase):

    @classmethod
    def setUpClass(cls):
        """
        Configuración inicial de la clase de pruebas.
        """
        super().setUpClass()
        cls.ResPartner = cls.env['res.partner']
        cls.country_pe = cls.env.ref('base.pe')
        cls.country_mx = cls.env.ref('base.mx')

    def setUp(self):
        """
        Configuración adicional antes de cada prueba.
        """
        super().setUp()
        self.env.company.country_id = self.country_pe

    def _create_view_arch(self, tag_names):
        """
        Crea un elemento XML de vista con las etiquetas especificadas.

        Args:
            tag_names (list): Lista de nombres de etiquetas o tuplas para crear el XML de la vista.

        Returns:
            etree._Element: Elemento XML de la vista creado.
        """    
        arch = etree.Element('form')
        for name in tag_names:
            if isinstance(name, tuple):
                tag = etree.SubElement(arch, name[0])
                tag.set('name', name[1])
            else:
                field = etree.SubElement(arch, 'field')
                field.set('name', name)
        return arch

    def _check_tags_visibility_view_arch(self, country, tags, check_visibility):
        """
        Verifica la visibilidad de las etiquetas en un elemento XML de vista en base a la configuración del país.

        Args:
            country: País o lista de países a comparar con el país de la compañía.
            tags (list): Lista de etiquetas cuya visibilidad se va a verificar.
            check_visibility (bool): True si se espera que las etiquetas sean visibles, False si se espera que estén ocultas.
        """
        
        # Construimos una vista con un campo y un grupo
        field_1 = 'field_1'
        group_1 = 'group_1'
        arch = self._create_view_arch([field_1, ('group', group_1)])
        
        countries = country if isinstance(country, list) else [country]

        arch, view = self.ResPartner._tags_invisible_per_country(arch, None, tags, countries)

        arch_field_1 = arch.xpath(f"//field[@name='{field_1}']")
        arch_group_1 = arch.xpath(f"//group[@name='{group_1}']")

        if check_visibility:
            self.assertFalse('invisible' in arch_field_1[0].attrib, f"El campo '{field_1}' no debe estar invisible.")
            self.assertFalse('invisible' in arch_group_1[0].attrib, f"El grupo con nombre: '{group_1}' no debe estar invisible.")
        else:
            self.assertTrue('invisible' in arch_field_1[0].attrib, f"El campo '{field_1}' debe estar invisible.")
            self.assertTrue('invisible' in arch_group_1[0].attrib, f"El grupo con nombre: '{group_1}' debe estar invisible.")

    def test_tags_visible_when_country_matches(self):
        """
        Prueba que las etiquetas sean visibles cuando el país de la compañia coincide con los países
        que se envían en la lista de la función self.ResPartner._tags_invisible_per_country.
        """
        self._check_tags_visibility_view_arch(
            country=self.country_pe, 
            tags=['field_1', ('group', 'group_1')], 
            check_visibility=True
        )

    def test_tags_invisible_when_country_does_not_match(self):
        """
        Prueba que las etiquetas no sean visibles cuando el país de la compañia no coincide con los países
        que se envían en la lista de la función self.ResPartner._tags_invisible_per_country.
        """
        self._check_tags_visibility_view_arch(
            country=self.country_mx, 
            tags=['field_1', ('group', 'group_1')], 
            check_visibility=False
        )
        
    def test_tags_visible_with_empty_tags_and_countries_lists(self):
        """
        Prueba que las etiquetas sean visibles cuando se envían vacios los parámetros de lista de etiquetas
        y lista de países a la función self.ResPartner._tags_invisible_per_country.
        """
        self._check_tags_visibility_view_arch(
            country=[], 
            tags=[], 
            check_visibility=True
        )

    def test_tags_visible_with_multiple_countries(self):
        """
        Prueba que las etiquetas sean visibles cuando el país de la compañia coincide con los múltiples países
        que se envían en la lista de la función self.ResPartner._tags_invisible_per_country.
        """
        self._check_tags_visibility_view_arch(
            country=[self.country_mx, self.country_pe], 
            tags=['field_1', ('group', 'group_1')], 
            check_visibility=True
        )
