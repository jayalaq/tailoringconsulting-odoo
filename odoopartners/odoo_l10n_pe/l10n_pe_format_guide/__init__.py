from . import models

# Esta funcion hook '_trasnfer_data_to_horario_almacen' se creo con la finalidad de transferir la informacion del campo que anteriormente se estaba usando de odoo studio 'x_studio_horario_atencin_almacn' al nuevo campo creado 'horario_almacen' en el modelo res.partner. Para versiones posteriores esa funcion hook debera ser eliminada ya que el campo anteriormente usando 'x_studio_horario_atencin_almacn' quedara obsoleto y ya no se utilizara.

def _trasnfer_data_to_horario_almacen(env):
    res_partners = env['res.partner']
    
    if 'x_studio_horario_atencin_almacn' in res_partners.fields_get():
        partners = res_partners.search([('x_studio_horario_atencin_almacn', '!=', False)])
        for partner in partners:
            old_value = getattr(partner, 'x_studio_horario_atencin_almacn', False)
            if old_value: 
                partner.write({'horario_almacen': old_value})
    else:
        return 