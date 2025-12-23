from . import models


def _uninstall_module_complete(env):
    env.cr.execute(
        """UPDATE ir_act_window 
           SET domain = '[]' 
           WHERE name->>'en_US' = 'Inventory Overview';
        """
    )
    env.cr.commit()
