# -*- coding: utf-8 -*-
import base64
import requests
from odoo import fields, models
from odoo.exceptions import ValidationError


class ClientSupport(models.TransientModel):
    _name = 'client.support'
    _description = 'Client Support'

    name = fields.Char(string='Nombre', required='True', help='Ingresa tu nombre')
    empresa = fields.Char(string='Empresa', required='True', help='Ingresa el nombre de tu empresa')
    odoo_bd = fields.Char(string='Tu URL de Odoo', required='True', help='Copia aquí el URL desde el que ingresas a odoo, example myempresa.ganemo.co')
    email = fields.Char(string='Email', required='True',
                        help='Ingresa tu email')
    description = fields.Text(string='Description', required='True',
                              help='Especifica el incidente con mucho detalle, empezando con los pasos necesarios para replicarlo, describiendo el comportamiento encontrado y finalmente cuál es el resultado esperado con la justificación.')
    #attachment_ids = fields.Many2many('ir.attachment', string='Attachments',
    #                                  help='Attach files related to your problem.')
    #support_type = fields.Selection([
    #    ('functional', 'Functional Support'),
    #    ('technical', 'Technical Support'), ], string="Support Type",
    #    required='True', default="technical", help='Select support type')

    #Esta parte todavía no hemos implementado un URL para los request, por lo tanto en la vista del Wizard de Helpdesk No se ha incluído el botón SUBMIT, para que los usuarios no puedan ejecutar esta función
    def confirm_button(self):
        """ Esta es la Función para crear el ticket en Ganemo """
        headers = {'Content-type': 'application/json'}
        response = requests.post(
            url='https://www.ganemo.co/help/request',
            json={
                'params': {
                    'customer_name': self.name,
                    'email': self.email,
                    'description': self.description,
                    'support_type': self.support_type,
                    'attachments': [
                        {
                            'data': base64.b64encode(rec.datas).decode('utf-8'),
                            'name': rec.name
                        } for rec in self.attachment_ids
                    ],
                }
            },
            headers=headers)
        response_status = response.json()
        if response_status['result']['message'] == 'success':
            return {
                'effect': {
                    'fadeout': 'slow',
                    'message': 'Ticket Created Successfully',
                    'type': 'rainbow_man',
                    'target': 'new',
                }
            }
        else:
            raise ValidationError(
                "The ticket submission did not go through. Please try again.")

    def whatsapp_button(self):
        """ Function for getting support through Whatsapp"""
        if self.description and self.name:
            name_string = ''
            empresa_string = ''
            odoo_bd_string = ''
            email_string = ''
            description_string = ''
            message_name = self.name.split(' ')
            message_empresa = self.empresa.split(' ')
            message_odoo_bd = self.odoo_bd.split(' ')
            message_email = self.email.split(' ')
            message_description = self.description.split(' ')
            for msgn in message_name:
                name_string = name_string + msgn + '%20'
            for msgp in message_empresa:
                empresa_string = empresa_string + msgp + '%20'
            for msgo in message_odoo_bd:
                odoo_bd_string = odoo_bd_string + msgo + '%20'
            for msge in message_email:
                email_string = email_string + msge + '%20'
            for msgd in message_description:
                description_string = description_string + msgd + '%20'
            msg_name_string = name_string[:(len(name_string) - 3)]
            msg_empresa_string = empresa_string[:(len(empresa_string) - 3)]
            msg_odoo_bd_string = odoo_bd_string[:(len(odoo_bd_string) - 3)]
            msg_email_string = email_string[:(len(email_string) - 3)]
            msg_description_string = description_string[:(len(description_string) - 3)]
            phone_number = str(+51964666869)
            return {
                'type': 'ir.actions.act_url',
                'url': "https://wa.me/" + phone_number + "?text=" + "Hola," + "%20"+ "soy" + "%20" + msg_name_string + "," + "%20" + "de la empresa" + "%20" + msg_empresa_string + 
                "%0A" + "Utilizo" + "%20" + "la" + "%20" + "BD:" + "%20" + msg_odoo_bd_string + 
                "%0A" + "Puedes" + "%20" + "responderme" + "%20" + "al" + "%20" + "e-mail:" + "%20" + msg_email_string + 
                "%0A" +
                "%0A" + "***DECLARACIÓN***" +
                "%0A" + "Acepto" + "%20" + "que" + "%20" + "las" + "%20" + "horas" + "%20" + "dedicadas" + "%20" + "a" + "%20" + "la" + "%20" + "atención" + "%20" + "de" + "%20" +
                "este" + "%20" + "incidente" + "%20" + "por" + "%20" + "parte" + "%20" + "de" + "%20" + "Ganemo," + "%20" + "se" + "%20" + "descuenten" + "%20" + "de" + "%20" + "mi" + "%20" +
                "pack" + "%20" + "de" + "%20" + "soporte" + "%20" + "o" + "%20" + "se" + "%20" + "me" + "%20" + "facturen" + "%20" + "a" + "%20" + "discreción" + "%20" + "de" + "%20" + "Ganemo." +
                "%0A" +
                "%0A" + "***DETALLE***DEL***TICKET***" +
                "%0A" + msg_description_string,
                'target': 'new',
                'res_id': self.id,
                'tag': 'reload',
            }
