from . import models


def _uninstall_module_complete(env):
    env.cr.execute("""UPDATE ir_act_window SET domain = '[]' WHERE ir_act_window.name->>'en_US' = 'Accounting Dashboard';""")
    env.cr.execute("""UPDATE ir_act_window SET domain = '[]' WHERE ir_act_window.name->>'en_US' = 'Journals';""")
