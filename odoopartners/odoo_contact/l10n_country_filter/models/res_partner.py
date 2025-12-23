from odoo import models


class ResPartner(models.Model):
    _inherit = 'res.partner'

    def _tags_invisible_per_country(self, arch, view, tags, countries):
        """
        Modifica la visibilidad de las etiquetas XML especificadas en el XML de la vista según el país de la empresa actual.

        Argumentos:
            arch (etree._Element): El elemento XML arch de la vista.
            view (etree._Element): El elemento XML de la vista.
            tags (lista): Lista de nombres de etiquetas o tuplas que representan consultas Xpath para etiquetas que se harán invisibles.
            countries (lista): Lista de referencias de países para verificar contra el país actual de la empresa.

        Devuelve:
            Tuple[etree._Element, etree._Element]: Los elementos arch y view modificados.

        Esta función verifica si el país de la empresa actual está en la lista proporcionada de países.
        Si es verdadero, devuelve el arch y view originales sin modificación. De lo contrario, itera a través
        de las etiquetas especificadas y hace invisibles los elementos correspondientes en el XML de arch.

        Ejemplo:
            Suponiendo que tags = ['ubigeo', ('group', 'extended_info')], countries = [self.env.ref('base.pe')],
            y el país actual de la empresa es 'Perú', la función modificará el XML de arch para hacer invisibles
            los elementos con consultas Xpath "//field[@name='ubigeo']" y "//group[@name='extended_info']".
        """
        country_company = self.env.company.country_id in countries
        if country_company:
            return arch, view
        for tag in tags:
            if isinstance(tag, tuple):
                value = "//{}[@name='{}']".format(tag[0], tag[1])
            else:
                value = "//field[@name='{}']".format(tag)
            for node in arch.xpath(value):
                node.set('invisible', '1')
        return arch, view
