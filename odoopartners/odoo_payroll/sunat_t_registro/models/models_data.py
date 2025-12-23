from odoo import api, fields, models
from odoo.osv import expression


class OtherAnnexedEstablishments(models.Model):
    _name = "other.annexed.establishments"
    _description = "Other Annexed Establishments"

    code = fields.Char(string='Código Establecimiento')
    name = fields.Char(string='Nombre')
    partner_id = fields.Many2one(comodel_name='res.partner', string='Contacto')
    employee_id = fields.Many2one(comodel_name='hr.employee', string='Contacto')

    @api.model
    def _name_search(self, name, args=None, operator='ilike', limit=100, name_get_uid=None, **kwargs):
        args = args or []
        domain = []
        if name:
            domain = ['|', ('code', '=ilike', name.split(' ')[0] + '%'), ('name', operator, name)]
            if operator in expression.NEGATIVE_TERM_OPERATORS:
                domain = ['&', '!'] + domain[1:]
        return self._search(expression.AND([domain, args]), limit=limit, access_rights_uid=name_get_uid)


class IndustrialClasification(models.Model):
    _name = 'international.industrial.classification'
    _description = 'Clasificación Industrial'

    code = fields.Char(string='Código CIIU')
    name = fields.Char(string='Descripción')

    @api.model
    def _name_search(self, name, args=None, operator='ilike', limit=100, name_get_uid=None, **kwargs):
        args = args or []
        domain = []
        if name:
            domain = ['|', ('code', '=ilike', name.split(' ')[0] + '%'), ('name', operator, name)]
            if operator in expression.NEGATIVE_TERM_OPERATORS:
                domain = ['&', '!'] + domain[1:]
        return self._search(expression.AND([domain, args]), limit=limit, access_rights_uid=name_get_uid)


class RoadTypeObject(models.Model):
    _name = "road.type.object"
    _description = "Road Type Object"

    code = fields.Char(string='N°')
    name = fields.Char(string='Descripción')

    @api.model
    def _name_search(self, name, args=None, operator='ilike', limit=100, name_get_uid=None, **kwargs):
        args = args or []
        domain = []
        if name:
            domain = ['|', ('code', '=ilike', name.split(' ')[0] + '%'), ('name', operator, name)]
            if operator in expression.NEGATIVE_TERM_OPERATORS:
                domain = ['&', '!'] + domain[1:]
        return self._search(expression.AND([domain, args]), limit=limit, access_rights_uid=name_get_uid)


class ZoneTypeObject(models.Model):
    _name = "zone.type.object"
    _description = "Zone Type Object"

    code = fields.Char(string='N°')
    name = fields.Char(string='Descripción')

    @api.model
    def _name_search(self, name, args=None, operator='ilike', limit=100, name_get_uid=None, **kwargs):
        args = args or []
        domain = []
        if name:
            domain = ['|', ('code', '=ilike', name.split(' ')[0] + '%'), ('name', operator, name)]
            if operator in expression.NEGATIVE_TERM_OPERATORS:
                domain = ['&', '!'] + domain[1:]
        return self._search(expression.AND([domain, args]), limit=limit, access_rights_uid=name_get_uid)


class UbigeoReniecObject(models.Model):
    _name = "ubigeo.reniec.object"
    _description = "Ubigeo Reniec Object"

    code = fields.Char(string='Código')
    name = fields.Char(string='Descripción')

    @api.model
    def _name_search(self, name, args=None, operator='ilike', limit=100, name_get_uid=None, **kwargs):
        args = args or []
        domain = []
        if name:
            domain = ['|', ('code', '=ilike', name.split(' ')[0] + '%'), ('name', operator, name)]
            if operator in expression.NEGATIVE_TERM_OPERATORS:
                domain = ['&', '!'] + domain[1:]
        return self._search(expression.AND([domain, args]), limit=limit, access_rights_uid=name_get_uid)


class OccupationalWorkerCategory(models.Model):
    _name = "occupational.worker.category"
    _description = "Occupational Worker Category"

    code = fields.Char(string='Código')
    name = fields.Char(string='Descripción')
    private_sector = fields.Char(string='Sector Privado')
    public_sector = fields.Char(string='Sector Público')
    other_entities = fields.Char(string='Otras Entidades')

    @api.model
    def _name_search(self, name, args=None, operator='ilike', limit=100, name_get_uid=None, **kwargs):
        args = args or []
        domain = []
        if name:
            domain = ['|', ('code', '=ilike', name.split(' ')[0] + '%'), ('name', operator, name)]
            if operator in expression.NEGATIVE_TERM_OPERATORS:
                domain = ['&', '!'] + domain[1:]
        return self._search(expression.AND([domain, args]), limit=limit, access_rights_uid=name_get_uid)


class WorkerTypePensionerProvider(models.Model):
    _name = "worker.type.pensioner.provider"
    _description = "Worker Type Pensioner Provider"

    code = fields.Char(string='Código')
    name = fields.Char(string='Descripción')
    abbreviated_name = fields.Char(string='Descripción abreviada')
    private_sector = fields.Char(string='Sector Privado')
    public_sector = fields.Char(string='Sector Público')
    other_entities = fields.Char(string='Otras Entidades')

    @api.model
    def _name_search(self, name, args=None, operator='ilike', limit=100, name_get_uid=None, **kwargs):
        args = args or []
        domain = []
        if name:
            domain = ['|', ('code', '=ilike', name.split(' ')[0] + '%'), ('name', operator, name)]
            if operator in expression.NEGATIVE_TERM_OPERATORS:
                domain = ['&', '!'] + domain[1:]
        return self._search(expression.AND([domain, args]), limit=limit, access_rights_uid=name_get_uid)

class EduNameObject(models.Model):
    _name = "edu.name.object"
    _description = "Edu Name Object"

    code = fields.Char(string='Código')
    name = fields.Char(string='Descripción')

    @api.model
    def _name_search(self, name, args=None, operator='ilike', limit=100, name_get_uid=None, **kwargs):
        args = args or []
        domain = []
        if name:
            domain = ['|', ('code', '=ilike', name.split(' ')[0] + '%'), ('name', operator, name)]
            if operator in expression.NEGATIVE_TERM_OPERATORS:
                domain = ['&', '!'] + domain[1:]
        return self._search(expression.AND([domain, args]), limit=limit, access_rights_uid=name_get_uid)


class EduCareerObject(models.Model):
    _name = "edu.career.object"
    _description = "Edu Career Object"

    code = fields.Char(string='Código')
    name = fields.Char(string='Descripción')

    @api.model
    def _name_search(self, name, args=None, operator='ilike', limit=100, name_get_uid=None, **kwargs):
        args = args or []
        domain = []
        if name:
            domain = ['|', ('code', '=ilike', name.split(' ')[0] + '%'), ('name', operator, name)]
            if operator in expression.NEGATIVE_TERM_OPERATORS:
                domain = ['&', '!'] + domain[1:]
        return self._search(expression.AND([domain, args]), limit=limit, access_rights_uid=name_get_uid)


class EduYearGraduationObject(models.Model):
    _name = "edu.year.graduation.object"
    _description = "Edu Year Graduation Object"

    code = fields.Char(string='Código')
    name = fields.Char(string='Descripción')

    @api.model
    def _name_search(self, name, args=None, operator='ilike', limit=100, name_get_uid=None, **kwargs):
        args = args or []
        domain = []
        if name:
            domain = ['|', ('code', '=ilike', name.split(' ')[0] + '%'), ('name', operator, name)]
            if operator in expression.NEGATIVE_TERM_OPERATORS:
                domain = ['&', '!'] + domain[1:]
        return self._search(expression.AND([domain, args]), limit=limit, access_rights_uid=name_get_uid)


class TypeFormativeModalityWork(models.Model):
    _name = "type.formative.modality.work"
    _description = "Type Formative Modality Work"

    code = fields.Char(string='Código')
    name = fields.Char(string='Descripción')
    abbreviated_name = fields.Char(string='Descripción abreviada')

    @api.model
    def _name_search(self, name, args=None, operator='ilike', limit=100, name_get_uid=None, **kwargs):
        args = args or []
        domain = []
        if name:
            domain = ['|', ('code', '=ilike', name.split(' ')[0] + '%'), ('name', operator, name)]
            if operator in expression.NEGATIVE_TERM_OPERATORS:
                domain = ['&', '!'] + domain[1:]
        return self._search(expression.AND([domain, args]), limit=limit, access_rights_uid=name_get_uid)


class OccupationWorkPersonnelTrainingModality(models.Model):
    _name = "occupation.work.personnel.training.modality"
    _description = "Occupation Work Personnel Training"

    code = fields.Char(string='Código')
    name = fields.Char(string='Descripción')

    @api.model
    def _name_search(self, name, args=None, operator='ilike', limit=100, name_get_uid=None, **kwargs):
        args = args or []
        domain = []
        if name:
            domain = ['|', ('code', '=ilike', name.split(' ')[0] + '%'), ('name', operator, name)]
            if operator in expression.NEGATIVE_TERM_OPERATORS:
                domain = ['&', '!'] + domain[1:]
        return self._search(expression.AND([domain, args]), limit=limit, access_rights_uid=name_get_uid)
