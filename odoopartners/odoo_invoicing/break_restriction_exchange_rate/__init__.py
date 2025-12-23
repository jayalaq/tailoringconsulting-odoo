from . import models

def post_init_hook(env):
    sql_query = """ALTER TABLE res_currency_rate DROP CONSTRAINT IF EXISTS res_currency_rate_unique_name_per_day;"""
    env.cr.execute(sql_query)
