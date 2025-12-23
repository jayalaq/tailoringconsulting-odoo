from . import models
from . import reports

def _post_init_hook(env):
    env["account.chart.template"].rent_4ta_post_init()