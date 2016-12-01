from core.db import ibs_db,ibs_query
from core.user import user_main
from core.ras import ras_main
from core.lib.time_lib import *
from core.lib.general import *
from core.snapshot import snapshot_defs, snapshot_main, onlines_loop
import time

class OnlinesSnapShotOnlinesLoopClient(onlines_loop.OnlinesLoopClient):
    def __init__(self):
        onlines_loop.OnlinesLoopClient.__init__(self, defs.SNAPSHOT_ONLINES_INTERVAL)
        self.__resetValues()

    def __resetValues(self):
        self.internet_onlines = self.__getRasIDsDic()
        self.voip_onlines = self.__getRasIDsDic()

    def loopEnd(self):
        internet_onlines = self.__filterZeroValues(self.internet_onlines)
        voip_onlines = self.__filterZeroValues(self.voip_onlines)

        self.__updateQuery(self.internet_onlines, self.voip_onlines).runQuery() 

        self.__resetValues()
    
    def __updateQuery(self, internet_onlines, voip_onlines):
        now = dbTimeFromEpoch(time.time())
        query = self.__insertToTableQuery(now, "internet_onlines_snapshot", internet_onlines)
        query += self.__insertToTableQuery(now, "voip_onlines_snapshot", voip_onlines)
        return query

    def __insertToTableQuery(self, _date, table_name, val_dic):
        """
            insert values for now in snapshot table
            val_dic(dic): dic in format {ras_id:value}
        """
        query = ibs_query.IBSQuery()
        for ras_id in val_dic:
            query += ibs_db.createInsertQuery(table_name,
                                               {"snp_date":dbText(_date),
                                                "ras_id":ras_id,
                                                "value":val_dic[ras_id]})
        return query

    def processInstance(self, user_obj, instance):
        ras_id, unique_id_val = user_obj.getGlobalUniqueID(instance)

        if user_obj.isNormalUser():
            self.internet_onlines[ras_id] += 1
        else:
            self.voip_onlines[ras_id] += 1

    def __getRasIDsDic(self):
        """
            return a dic in format {ras_id:0}
            all loaded ras_ids will be added in dic
        """
        _dic = {}
        for ras_id in ras_main.getLoader().getAllRasIDs():
            _dic[ras_id] = 0
        return _dic

    def __filterZeroValues(self, _dic):
        for ras_id in _dic.keys():
            if _dic[ras_id] == 0:
                del(_dic[ras_id])
        return _dic

