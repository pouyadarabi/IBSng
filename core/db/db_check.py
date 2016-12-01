from core.db import dbpool
from core.event import periodic_events
from core import defs

def init():
    db_pool_check=DBPoolCheck('dbcheck',defs.DB_POOL_CHECK_INTERVAL,[],1)
    periodic_events.getManager().register(db_pool_check)

class DBPoolCheck(periodic_events.PeriodicEvent):
    def run(self):
        dbpool.getPool().check()