from . import models
from . import wizards


def _edocument_post_init(env):
    env['account.chart.template']._edocument_post_init()
