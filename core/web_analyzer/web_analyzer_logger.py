from core.db import ibs_db, ibs_query
from core.lib.general import *
from core.lib.time_lib import *
from core.ibs_exceptions import *
from core.user import user_main


TIMESTAMP = 0
URL = 1
ELAPSED = 2
BYTES = 3
MISSED = 4
SUCCESSFUL = 5
COUNT = 6

DEBUG = False

class WebAnalyzerLogger:
    def logAnalysis(self, log_dict):
        """
            log_dict(dict):{user_ip:[[request_details], ...]}
            Insert web request into db
        """
        query = ibs_query.IBSQuery()
        for ip in log_dict:
            user_id = self.__getUserIDForIP(ip)
            
            if DEBUG:
                toLog("logAnalysis: user_id is %s"%user_id, LOG_DEBUG)
                
            if user_id != None:
                self.__logRecords(ip, user_id, log_dict[ip], query)
        query.runQuery()
        
    def __logRecords(self,ip, user_id, records, query):
        for record in records:
            try:
                query += self.__logAnalysisQuery( ip,
                                                 user_id,
                                                 record[TIMESTAMP],
                                                 record[URL],
                                                 record[ELAPSED],
                                                 record[BYTES],
                                                 record[MISSED][0],
                                                 record[MISSED][1],
                                                 record[SUCCESSFUL][0],
                                                 record[SUCCESSFUL][1],
                                                 record[COUNT]
                                            )
            except:
                logException(LOG_ERROR)
    
    
    def __getUserIDForIP(self,ip):
        """
            returns user_id associated to user_ip, None otherwise
        """
        return user_main.getIPMap().getUserIDForIP(ip)
        
    def __logAnalysisQuery(self, ip, user_id, timestamp, url, elapsed, bytes, miss, hit, successful, failure, _count):
        return ibs_db.createFunctionCallQuery("insert_web_analyzer_log", \
                                                ("%s"%dbText(dbTimeFromEpoch(to_float(timestamp, 'timestamp'))),
                                                 "%s::bigint"%user_id,
                                                 dbText(ip),
                                                 dbText(url), 
                                                 to_int(elapsed,'elapsed'), 
                                                 to_int(bytes,'bytes'), 
                                                 "%s::smallint"%to_int(miss, 'misses'),
                                                 "%s::smallint"%to_int(hit, 'hits'),
                                                 "%s::smallint"%to_int(successful, 'successful'),
                                                 "%s::smallint"%to_int(failure , 'failure'),
                                                 to_int(_count,'count')
                                                )
                                              )
