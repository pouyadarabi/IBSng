from core.db import ibs_db,ibs_query
from core.user import user_main
from core.ras import ras_main
from core.lib.time_lib import *
from core.lib.general import *
from core.snapshot import snapshot_defs,snapshot_main,onlines_loop
import time

class BWSnapShotOnlinesLoopClient(onlines_loop.OnlinesLoopClient):
    def __init__(self):
        onlines_loop.OnlinesLoopClient.__init__(self, defs.SNAPSHOT_BW_INTERVAL)
        self.__resetValues()

    def __resetValues(self):
        self.onlines_bw = {}

    def processInstance(self, user_obj, instance):
    
        if user_obj.getUserAttrs().hasAttr("save_bw_usage") and user_obj.isNormalUser():
            _in,out,in_rate,out_rate = user_obj.getTypeObj().getInOutBytes(instance)

            if in_rate > 0 or out_rate > 0:
            
                user_id = user_obj.getUserID()
                
                if self.onlines_bw.has_key(user_id):
                    self.onlines_bw[user_id][0] += in_rate
                    self.onlines_bw[user_id][1] += out_rate
                else:
                    self.onlines_bw[user_id] = [in_rate, out_rate]
            
    def loopEnd(self):
        self.insertToTableQuery("internet_bw_snapshot", self.onlines_bw).runQuery()     
        self.__resetValues()

    def insertToTableQuery(self, table_name, val_dic):
        """
            insert values for now in snapshot table
        """
        date = dbText(dbTimeFromEpoch(time.time()))
        query = ibs_query.IBSQuery()
        createInsertQuery = ibs_db.createInsertQuery
        
        for user_id in val_dic:
            query += createInsertQuery(table_name,
                                       {"snp_date" : date,
                                        "user_id" : user_id,
                                        "in_rate" : int(val_dic[user_id][0]),
                                        "out_rate" : int(val_dic[user_id][1])
                                       }
                                      )
        return query
        