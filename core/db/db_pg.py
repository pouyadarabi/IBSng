from core import ibs_exceptions
from core.db.ibs_db import *
import pg
import time

try:
    from pg import error as PGError
except ImportError:
    from pg import Error as PGError

class db_pg (ibs_db):
    
    def connect(self,dbname,host,port,user,password):
        try:
            self.connHandle=pg.connect(dbname,host,port,None,None,user,password)
        except Exception,e:
            raise ibs_exceptions.DBException(str(e))
        except PGError,e:
            raise ibs_exceptions.DBException(str(e))

    def prepareQuery(self,plan_name, args , query):
        self._runQuery("prepare %s (%s) as %s"%(plan_name,",".join(args),query))

    def executePrepared(self, plan_name, values):
        return self.selectQuery("execute %s (%s)"%(plan_name,",".join(map(str,values))))

    def _runQueryDB(self,query):
        """
            run the query , no exception handling done here
            return result set of query
        """
        connection=self.getConnection()
        return connection.query(query)
        
    def transactionQuery(self,query):
        ibs_db.transactionQuery(self,query)
        query_len=len(query)
        if query_len>4000:
            self.__transactionQuery("BEGIN;")
            sent=0
            while sent<query_len:
                end=(sent+4000,query_len)[sent+4000>query_len]
                while query[end-1]!=";": end+=1
                self.__transactionQuery(query[sent:end])
                sent=end
            self.__transactionQuery("COMMIT;")
        else:
            return self.__transactionQuery("BEGIN; %s COMMIT;"%query)
    
    def __transactionQuery(self,command):
        try:
            return self._runQuery(command)
        except PGError,e:
            try:
                self._runQuery("ABORT;")
            except:
                pass
        
            raise ibs_exceptions.DBException("%s query: %s" %(e,command))

        except Exception,e:
            try:
                self._runQuery("ABORT;")
            except:
                pass
            logException(LOG_ERROR)

            raise ibs_exceptions.DBException("%s query: %s" %(e,command))

    def query(self,command):
        try:
            return self._runQuery(command)
        except PGError,e:
            raise ibs_exceptions.DBException("%s query: %s" %(e,command))

        except Exception,e:
            raise ibs_exceptions.DBException("%s query: %s" %(e,command))

    def runIBSQuery(self,ibs_query):
        self.__transactionQuery("BEGIN;")
        map(self.__transactionQuery,ibs_query)
        self.__transactionQuery("COMMIT;")
    
    def check(self):
        try:
            self.query("BEGIN;ROLLBACK;")
        except Exception,e:
            try:
                self.reset()
            except Exception,e:
                raise ibs_exceptions.DBException("check function on reseting connection %s"%e)
            except PGError,e:
                raise ibs_exceptions.DBException("check function on reseting connection %s"%e)
    