from core.DBconnect import connect_to_sql

def sql_run(datasource, pushdownQuery):
    sp = connect_to_sql(datasource, pushdownQuery)
    sdf = sp.run()
    return sdf
