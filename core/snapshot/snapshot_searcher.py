from core.report.search_helper import SearchHelper
from core.report.search_table import SearchTable
from core.report.search_group import SearchGroup
from core.snapshot import snapshot_defs
from core.ras import ras_main
from core.db import db_main
from core.lib.date import *
from core.lib.time_lib import *
from core.lib.multi_strs import MultiStr
from core import defs

import time

class OnlineSnapShotSearchTable(SearchTable):
    def createQuery(self):
        if not self.getRootGroup().isEmpty():
            cond = self.getRootGroup().getConditionalClause()
        else:
            cond = "true"

        table_name=self.getTableName()
        return "select extract(epoch from snp_date) as _date, sum(value) as val from %s where %s group by snp_date order by snp_date asc"%(table_name, cond)
        

class InternetSnapShotSearchTable(OnlineSnapShotSearchTable):
    def __init__(self):
        SearchTable.__init__(self,"internet_onlines_snapshot")
        
class VoIPSnapShotSearchTable(OnlineSnapShotSearchTable):
    def __init__(self):
        SearchTable.__init__(self,"voip_onlines_snapshot")

class BWSnapShotSearchTable(SearchTable):
    def __init__(self):
        SearchTable.__init__(self,"internet_bw_snapshot")

    def createQuery(self):
        if not self.getRootGroup().isEmpty():
            cond = self.getRootGroup().getConditionalClause()
        else:
            cond = "true"

        table_name=self.getTableName()
        return "select extract(epoch from snp_date) as _date, sum(in_rate), sum(out_rate) from %s where %s group by snp_date order by snp_date asc"%(table_name, cond)

class SnapShotSearchHelper(SearchHelper):
    def __init__(self,conds,requester_obj,requester_role, _type):
        """
            _type(str) can be one of "internet" or "voip"
        """
        if _type == "internet":
            table = InternetSnapShotSearchTable()
        elif _type == "voip":
            table = VoIPSnapShotSearchTable()
        else:
            table = BWSnapShotSearchTable()
        
        self._type = _type
        
        SearchHelper.__init__(self,conds,requester_obj,requester_role,
                                                    {"snapshot":table})

    def getSnapShots(self):
        result = self.__getResult()
        return self.__fixStartEndDates(result)

    def __getResult(self):
        return db_main.getHandle().selectQuery(self.getTable("snapshot").createQuery(),1)

    def __getZeroValue(self,date):
        if self._type == "bw":
            return (date,0,0)
        else:
            return (date,0)

    def __fixStartEndDates(self, result):
        if self.hasCondFor("date_from","date_from_unit"):
            _from = AbsDateWithUnit(self.getCondValue("date_from"), self.getCondValue("date_from_unit")).getEpochDate()

            if not len(result) or result[0][0] > _from + defs.SNAPSHOT_ONLINES_INTERVAL*2:
                result.insert(0,self.__getZeroValue(_from))

        if self.hasCondFor("date_to","date_to_unit"):
            to = AbsDateWithUnit(self.getCondValue("date_to"), self.getCondValue("date_to_unit")).getEpochDate()
        else:
            to = time.time()

        if not len(result) or result[-1][0] < to - defs.SNAPSHOT_ONLINES_INTERVAL*2:
            result.append(self.__getZeroValue(to))
        
        return result


class SnapShotSearcher:
    def __init__(self,conds,requester_obj,requester_role,_type):
        self.search_helper=SnapShotSearchHelper(conds,requester_obj,requester_role,_type)
        self._type = _type
        
    ##############################################
    def applyConditions(self):
        """
            Apply conditions on tables, should check conditions here
        """
        table = self.search_helper.getTable("snapshot")
        if self._type == "bw":
            table.exactSearch(self.search_helper, "user_id", "user_id", MultiStr)
        else:
            table.exactSearch(self.search_helper,"ras_ips","ras_id",lambda ras_ip:ras_main.getLoader().getRasByIP(ras_ip).getRasID())
            
        self.checkSnapShotDuration()

        self.search_helper.setCondValue("date_from_op",">=")    
        table.dateSearch(self.search_helper,"date_from","date_from_unit","date_from_op","snp_date")

        self.search_helper.setCondValue("date_to_op","<")
        table.dateSearch(self.search_helper,"date_to","date_to_unit","date_to_op","snp_date")

    def checkSnapShotDuration(self):
        """
            don't allow duration of snapshot to be less that 20 minutes
        """
        if self.search_helper.hasCondFor("date_from","date_from_unit"):
            _from = AbsDateWithUnit(self.search_helper.getCondValue("date_from"), self.search_helper.getCondValue("date_from_unit")).getEpochDate()

            if self.search_helper.hasCondFor("date_to","date_to_unit"):
                to = AbsDateWithUnit(self.search_helper.getCondValue("date_to"), self.search_helper.getCondValue("date_to_unit")).getEpochDate()
            else:
                to = time.time()

            if to - _from <20*60:
                self.search_helper.setCondValue("date_from", dbTimeFromEpoch(to - 20*60))
                self.search_helper.setCondValue("date_from_unit", "gregorian")
    

    #################################################
    def getSnapShots(self):
        """
            return a list of snapshots [(date,value),...]
        """
        self.applyConditions()
        return self.search_helper.getSnapShots()


