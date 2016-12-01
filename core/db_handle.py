from core.db_conf import *
def getDBHandle():
    from core.db import db_pg
    return db_pg.db_pg("IBSng",DB_HOST,DB_PORT,DB_USERNAME,DB_PASSWORD)
