from core.report.search_helper import SearchHelper
from core.report.search_table import SearchTable,SearchAttrsTable
from core.report.search_group import SearchGroup
from core.lib.multi_strs import MultiStr
from core.lib import report_lib
from core.lib.date import AbsDate
from core.lib.general import *
from core.admin import admin_main
from core.user import user_main
from core.ras import ras_main
from core.ibs_exceptions import *
from core.errors import errorText
from core.db import db_main
from core.group import group_main
import types

class ConnectionLogSearchTable(SearchTable):
    def __init__(self):
        SearchTable.__init__(self,"connection_log")
        
    def createQuery(self):
        if not self.getRootGroup().isEmpty():
            table_name=self.getTableName()
            return "select connection_log_id from %s where %s"%(table_name,self.getRootGroup().getConditionalClause())

class ConnectionLogDetailsSearchTable(SearchAttrsTable):
    def __init__(self):
        SearchAttrsTable.__init__(self,"connection_log_details", "name", "value")
        
    def createQuery(self):
        if not self.getRootGroup().isEmpty():
            table_name=self.getTableName()
            return "select details.connection_log_id from \
                    (select connection_log_id,count(connection_log_id) as count from %s where %s group by connection_log_id) as details \
                    where details.count=%s"% (table_name,self.getRootGroup().getConditionalClause(), len(self.getAttrs()))
        

class ConnectionSearchHelper(SearchHelper):
    def __init__(self,conds,requester_obj,requester_role):
        SearchHelper.__init__(self,conds,requester_obj,requester_role,
                                                     {"connection_log":ConnectionLogSearchTable(),
                                                    "connection_log_details":ConnectionLogDetailsSearchTable()})

    def getConnectionLogs(self,_from,to,order_by,desc,date_type):
        if self.getTable("connection_log_details").getRootGroup().isEmpty():
            return self._getConnectionLogsByDirectQuery(_from,to,order_by,desc,date_type)
        else:
            return self._getConnectionLogsByTempTable(_from,to,order_by,desc,date_type)


    def _getConnectionLogsByDirectQuery(self, _from,to,order_by,desc,date_type):
        """
            get connection logs by directly query the table 
            this is faster than creating temp table, but possible if we have only
            conditions from connection_log table
        """
        conditions = self.getTable("connection_log").getRootGroup().getConditionalClause()
        total_rows = self.__directQueryGetTotalResultsCount(conditions)
        if total_rows==0:
            return (0,0,"00:00:00",0,0,[])
            
        total_credit_used = self.__directQueryGetTotalCreditUsed(conditions)
        total_duration = self.__directQueryGetTotalDuration(conditions)
        total_in, total_out = self.__directQueryGetTotalInOuts(conditions)

        connections=self.__directQueryGetConnections(conditions,_from,to,order_by,desc)
        connection_details=self.__getConnectionDetails(db_main.getHandle(),connections)
            
        return (total_rows, total_credit_used, total_duration, total_in, total_out, 
                self.__createReportResult(connections,connection_details,date_type))
        
    def __directQueryGetConnections(self,conditions,_from,to,order_by,desc):
        return db_main.getHandle().get("connection_log",
                             conditions,
                             _from,
                             to,
                             (order_by,desc),
                             ["*",
                              "extract(epoch from logout_time-login_time) as duration_seconds"
                             ]
                            )

    def __directQueryGetTotalResultsCount(self, conditions):
        return db_main.getHandle().getCount("connection_log", conditions)

    def __directQueryGetTotalCreditUsed(self, conditions):
        if self.hasCondFor("show_total_credit_used"):
            return db_main.getHandle().get("connection_log",conditions,0,-1,"",["sum(credit_used) as sum"])[0]["sum"]
        return -1

    def __directQueryGetTotalDuration(self, conditions):
        if self.hasCondFor("show_total_duration"):
            return db_main.getHandle().get("connection_log",conditions,0,-1,"",["extract(epoch from sum(logout_time-login_time)) as sum"])[0]["sum"]
        return -1

    def __directQueryGetTotalInOuts(self, conditions):
        if self.hasCondFor("show_total_inouts"):
            return self.__getTotalInOutsFromTable(db_main.getHandle(), "connection_log", conditions)
        return -1, -1

    #################################################### shared functions
    def __getTotalInOutsFromTable(self, db_handle, table_name, cond="true"):
        """
            return a tuple of (total_in, total_out) by querying connection_log_ids from "table_name" using condition "cond"
        """
        if not cond:
            cond = "true"
            
        query = "select sum(value::bigint) as sum from connection_log_details where name='%s' and connection_log_id in (select %s.connection_log_id from %s where %s)"
        total_in = db_handle.selectQuery(query%("bytes_in", table_name, table_name, cond))[0]["sum"]
        total_out = db_handle.selectQuery(query%("bytes_out", table_name, table_name, cond))[0]["sum"]
        
        if total_in == None or total_out == None:
            total_in = 0
            total_out = 0

        return total_in, total_out
        
    def __createReportResult(self,connections,connection_details,date_type):
        details_dic=self.__convertConnectionDetailsToDic(connection_details)
        self.__repairConnectionsDic(connections,details_dic,date_type)
        return connections
        
    def __repairConnectionsDic(self,connections,details_dic,date_type):
        for connection in connections:
            connection["login_time_formatted"]=AbsDate(connection["login_time"],"gregorian").getDate(date_type)
            connection["logout_time_formatted"]=AbsDate(connection["logout_time"],"gregorian").getDate(date_type)

            try:
                connection["ras_description"]=ras_main.getLoader().getRasByID(connection["ras_id"]).getRasDesc()
            except GeneralException:
                connection["ras_description"]="id:%s"%connection["ras_id"]
                
            connection["service_type"]=user_main.getConnectionLogManager().getIDType(connection["service"])
            try:
                connection["details"]=details_dic[connection["connection_log_id"]]
            except KeyError:
                connection["details"]=[]
    
        return connections
        
    def __convertConnectionDetailsToDic(self,connection_details):
        details_dic={}
        last_id=None
        per_detail_list=[]
        
        for detail in connection_details:
            if last_id!=detail["connection_log_id"]:
                if last_id!=None:
                    details_dic[last_id]=per_detail_list
                last_id=detail["connection_log_id"]
                per_detail_list=[]
            per_detail_list.append((detail["name"],detail["value"]))

        if last_id!=None:
            details_dic[last_id]=per_detail_list

        return details_dic
                
    def __getConnectionDetails(self,db_handle,connections):
        details = []
        connection_log_ids = []
        i = 0
        for _list in connections:
            connection_log_ids.append(str(_list["connection_log_id"]))
            if (i and i%defs.POSTGRES_MAGIC_NUMBER==0) or i==len(connections)-1:
                details += db_handle.get("connection_log_details",
                             "connection_log_id in (%s)"%",".join(map(lambda x:"%s::bigint"%x,connection_log_ids)),
                             0,-1,"connection_log_id,name desc")
                connection_log_ids=[]
            i+=1

        return details

    ##########################################################################
    def _getConnectionLogsByTempTable(self, _from,to,order_by,desc,date_type):
        """
            temp table creation is more expensive but required if we have conditions
            on multiple tables
        """
        db_handle=db_main.getHandle(True)
        try:
            self.__createTempTable(db_handle)
            total_rows=self.__tempTableGetTotalResultsCount(db_handle)
            if total_rows==0:
                return (0,0,"00:00:00",0,0,[])
                
            total_credit_used = self.__tempTableGetTotalCreditUsed(db_handle)
            total_duration = self.__tempTableGetTotalDuration(db_handle)
            total_in, total_out = self.__tempTableGetTotalInOuts(db_handle)
            connections = self.__tempTableGetConnections(db_handle,_from,to,order_by,desc)
            connection_details = self.__getConnectionDetails(db_handle,connections)
        finally:
            try:
                self.dropTempTable(db_handle,"connection_log_report")
            except:
                logException(LOG_DEBUG)
                
            db_handle.releaseHandle()
            
        return (total_rows, total_credit_used, total_duration, total_in, total_out, 
                self.__createReportResult(connections,connection_details,date_type))


    def __tempTableGetConnections(self,db_handle,_from,to,order_by,desc):
        return db_handle.get("connection_log",
                             "connection_log.connection_log_id in (select connection_log_report.connection_log_id from connection_log_report)",
                             _from,
                             to,
                             (order_by,desc),
                             ["*",
                              "extract(epoch from logout_time-login_time) as duration_seconds"
                             ]
                            )
                      
    def __createTempTable(self,db_handle):
        select_query=self.__createConnectionLogIDsQuery()
        self.createTempTableAsQuery(db_handle,"connection_log_report",select_query)

    def __tempTableGetTotalResultsCount(self,db_handle):
        return db_handle.getCount("connection_log_report","true")

    def __tempTableGetTotalCreditUsed(self,db_handle):
        if self.hasCondFor("show_total_credit_used"):
            return db_handle.selectQuery("select sum(credit_used) as sum from connection_log,connection_log_report where \
                                           connection_log.connection_log_id=connection_log_report.connection_log_id")[0]["sum"]
        return -1

    def __tempTableGetTotalDuration(self,db_handle):
        if self.hasCondFor("show_total_duration"):
            return db_handle.selectQuery("select extract(epoch from sum(logout_time-login_time)) as sum from connection_log,connection_log_report where \
                                           connection_log.connection_log_id=connection_log_report.connection_log_id")[0]["sum"]
        return -1

    def __tempTableGetTotalInOuts(self,db_handle):
        if self.hasCondFor("show_total_inouts"):
            return self.__getTotalInOutsFromTable(db_handle, "connection_log_report", "true")
        return -1, -1
    
    def __createConnectionLogIDsQuery(self):
        return self.createGetIDQuery("select connection_log_id from connection_log")


    ################################################### Durations Analysis
    def getDurations(self):
        """
            return a list in format [[duration_seconds,count],...}
        """
        db_handle=db_main.getHandle(True)
        try:
            self.__createDurationsTempTable(db_handle)
            return self.__getDurations(db_handle)    
        finally:
            try:
                self.dropTempTable(db_handle,"durations_report")
            except:
                logException(LOG_DEBUG)

            db_handle.releaseHandle()

    def __createDurationsTempTable(self,db_handle):
        self.__createConnectionTempTable(db_handle,"durations_report")

    def __createConnectionTempTable(self,db_handle, table_name):
        select_query=self.createGetIDQuery("select connection_log_id from connection_log")
        self.createTempTableAsQuery(db_handle,table_name,select_query)

    def __getDurations(self, db_handle):
        duration_list=[[0,0],[60,0],[300,0],[3600,0],[7200,0],[14400,0]] #[end interval seconds, ]
        for i in range(len(duration_list)):
            cond=""
            if i==len(duration_list)-1:
                cond="logout_time-login_time >= interval '%s seconds'"%duration_list[i][0]
            else:
                cond="logout_time-login_time >= interval '%s seconds' and logout_time-login_time < interval '%s seconds'"%(duration_list[i][0],duration_list[i+1][0])

            duration_list[i][1]=db_handle.selectQuery("select count(*) from durations_report,connection_log \
                                            where durations_report.connection_log_id=connection_log.connection_log_id and %s"%cond)[0]["count"]
            
        return duration_list

    ############################################## Group Analysis
    def getGroupUsages(self):
        """
            return a list in format (group_name,duration)
            NOTE: currently this uses temp table creation, but using the table only once
                  maybe joining the tables produce better results
        """
        db_handle=db_main.getHandle(True)
        try:
            self.__createGroupUsagesTempTable(db_handle)
            return self.__getGroupUsagesDB(db_handle)    
        finally:
            try:
                self.dropTempTable(db_handle,"group_usages")
            except:
                logException(LOG_DEBUG)

            db_handle.releaseHandle()

    def __createGroupUsagesTempTable(self, db_handle):
        self.__createConnectionTempTable(db_handle,"group_usages")

    def __getGroupUsagesDB(self, db_handle):
        db_usages=db_handle.selectQuery("select group_id,extract(epoch from sum(logout_time-login_time)) as duration \
                                        from \
                                        group_usages,connection_log,users \
                                        where \
                                        connection_log.connection_log_id=group_usages.connection_log_id and \
                                        users.user_id=connection_log.user_id group by group_id")
        return self.__fixGroupNames(db_usages)
    
    def __fixGroupNames(self, db_usages):
        group_usages=[]
        for row in db_usages:
            group_name=group_main.getLoader().getGroupByID(row["group_id"]).getGroupName()
            group_usages.append((group_name,row["duration"]))
    
        return group_usages

    ############################################## Ras Analysis
    def getRasUsages(self):
        """
            return a list in format (ras_ip,duration)
        """
        db_handle=db_main.getHandle(True)
        try:
            self.__createRasUsagesTempTable(db_handle)
            return self.__getRasUsagesDB(db_handle)
        finally:
            try:
                self.dropTempTable(db_handle,"ras_usages")
            except:
                logException(LOG_DEBUG)

            db_handle.releaseHandle()

    def __createRasUsagesTempTable(self, db_handle):
        self.__createConnectionTempTable(db_handle,"ras_usages")

    def __getRasUsagesDB(self, db_handle):
        db_usages=db_handle.selectQuery("select ras_id,extract(epoch from sum(logout_time-login_time)) as duration \
                                        from \
                                        ras_usages,connection_log \
                                        where \
                                        connection_log.connection_log_id=ras_usages.connection_log_id\
                                        group by ras_id")
        return self.__fixRasIPs(db_usages)
    
    def __fixRasIPs(self, db_usages):
        ras_usages=[]
        for row in db_usages:
            ras_ip=ras_main.getLoader().getRasByID(row["ras_id"]).getRasIP()
            ras_usages.append((ras_ip,row["duration"]))
    
        return ras_usages

    ############################################## Voip Disconnect Cause Analysis
    def getVoIPDisconnectCauses(self):
        """
            return a list in format (diconnect_cause_code,count)
        """
        db_handle=db_main.getHandle(True)
        try:
            self.__createVoIPDisconnectCausesTempTable(db_handle)
            return self.__getVoIPDisconnectCausesDB(db_handle)
        finally:
            try:
                self.dropTempTable(db_handle,"voip_disconnect_causes_temp")
            except:
                logException(LOG_DEBUG)

            db_handle.releaseHandle()

    def __createVoIPDisconnectCausesTempTable(self, db_handle):
        self.__createConnectionTempTable(db_handle,"voip_disconnect_causes_temp")

    def __getVoIPDisconnectCausesDB(self, db_handle):
        db_causes=db_handle.selectQuery("select value,count(value) as count \
                                        from \
                                        connection_log_details,voip_disconnect_causes_temp \
                                        where \
                                        connection_log_details.connection_log_id=voip_disconnect_causes_temp.connection_log_id and \
                                        name='disconnect_cause' \
                                        group by value order by value")
        return self.__fixDisconnectCauses(db_causes)
    
    def __fixDisconnectCauses(self, db_causes):
        dc_causes=[]
        for row in db_causes:
            dc_causes.append((row["value"],row["count"]))
    
        return dc_causes

    ############################################## Successful connection Analysis
    def getSuccessfulCounts(self):
        """
            return a tuple (successful_count,failure_count)
        """
        db_handle=db_main.getHandle(True)
        try:
            self.__createSuccessfulCountsTempTable(db_handle)
            return self.__getSuccessfulCountsDB(db_handle)
        finally:
            try:
                self.dropTempTable(db_handle,"successful_count_temp")
            except:
                logException(LOG_DEBUG)

            db_handle.releaseHandle()

    def __createSuccessfulCountsTempTable(self, db_handle):
        self.__createConnectionTempTable(db_handle,"successful_count_temp")

    def __getSuccessfulCountsDB(self, db_handle):
        db_counts=db_handle.selectQuery("select successful,count(successful) as count\
                                        from \
                                        successful_count_temp,connection_log \
                                        where \
                                        successful_count_temp.connection_log_id=connection_log.connection_log_id \
                                        group by successful")
        return self.__fixSuccessfulCounts(db_counts)
    
    def __fixSuccessfulCounts(self, db_counts):
        success=0
        fails=0
        for row in db_counts:
            if row["successful"]=="t":
                success=row["count"]
            else:
                fails=row["count"]
    
        return (success,fails)

    ############################################## Admin Analysis
    def getAdminUsages(self):
        """
            return a list in format [(admin_name,duration)]
        """
        db_handle=db_main.getHandle(True)
        try:
            self.__createAdminUsagesTempTable(db_handle)
            return self.__getAdminUsagesDB(db_handle)    
        finally:
            try:
                self.dropTempTable(db_handle,"admin_usages_temp")
            except:
                logException(LOG_DEBUG)

            db_handle.releaseHandle()

    def __createAdminUsagesTempTable(self, db_handle):
        self.__createConnectionTempTable(db_handle,"admin_usages_temp")

    def __getAdminUsagesDB(self, db_handle):
        db_usages=db_handle.selectQuery("select owner_id,extract(epoch from sum(logout_time-login_time)) as duration \
                                        from \
                                        admin_usages_temp,connection_log,users \
                                        where \
                                        connection_log.connection_log_id=admin_usages_temp.connection_log_id and \
                                        users.user_id=connection_log.user_id group by owner_id")
        return self.__fixAdminNames(db_usages)
    
    def __fixAdminNames(self, db_usages):
        admin_usages=[]
        for row in db_usages:
            admin_name=admin_main.getLoader().getAdminByID(row["owner_id"]).getUsername()
            admin_usages.append((admin_name,row["duration"]))
    
        return admin_usages


class BaseConnectionLogSearcher:
    """
        Base Class than is used in Connection Log And Connection Usage Searchers
    """
    
    def applyConditions(self):
        con_table=self.search_helper.getTable("connection_log")

        self.__addUserIDCondition(con_table)

        con_table.ltgtSearch(self.search_helper,"credit_used","credit_used_op","credit_used")
    
        self.search_helper.setCondValue("login_time_from_op",">=")      
        con_table.dateSearch(self.search_helper,"login_time_from","login_time_from_unit","login_time_from_op","login_time")

        self.search_helper.setCondValue("login_time_to_op","<") 
        con_table.dateSearch(self.search_helper,"login_time_to","login_time_to_unit","login_time_to_op","login_time")

        self.search_helper.setCondValue("logout_time_from_op",">=")     
        con_table.dateSearch(self.search_helper,"logout_time_from","logout_time_from_unit","logout_time_from_op","logout_time")

        self.search_helper.setCondValue("logout_time_to_op","<")        
        con_table.dateSearch(self.search_helper,"logout_time_to","logout_time_to_unit","logout_time_to_op","logout_time")
        
        con_table.exactSearch(self.search_helper,"successful","successful",lambda yesno:{"yes":"t","no":"f"}[yesno.lower()])

        con_table.exactSearch(self.search_helper,"service","service",lambda _type:user_main.getConnectionLogManager().getTypeValue(_type))

        con_table.exactSearch(self.search_helper,"ras_ip","ras_id",lambda ras_ip:ras_main.getLoader().getRasByIP(ras_ip).getRasID())

    def __addUserIDCondition(self,con_table):
        if self.search_helper.isRequesterAdmin():
            admin_restricted=not self.search_helper.getRequesterObj().isGod() and self.search_helper.getRequesterObj().getPerms()["SEE CONNECTION LOGS"].isRestricted()
            if admin_restricted or self.search_helper.hasCondFor("owner"):
                if admin_restricted:
                    owner_ids=(self.search_helper.getRequesterObj().getAdminID(),)
                else:
                    owner_name=self.search_helper.getCondValue("owner")
                    if type(owner_name)==types.StringType:
                        owner_name=(owner_name,)
                    owner_ids=map(lambda owner_name:admin_main.getLoader().getAdminByName(owner_name).getAdminID(),owner_name)
            
                sub_query=self.__userOwnersConditionQuery(owner_ids)
                con_table.getRootGroup().addGroup(sub_query)
        
        con_table.exactSearch(self.search_helper,"user_ids","user_id",MultiStr,"bigint")        

    def __userOwnersConditionQuery(self,owner_ids):
        cond_group=SearchGroup("or")
        map(lambda owner_id:cond_group.addGroup("users.owner_id=%s"%owner_id),owner_ids)
        return "connection_log.user_id in (select user_id from users where %s)"%cond_group.getConditionalClause()

        
class ConnectionSearcher(BaseConnectionLogSearcher):
    def __init__(self,conds,requester_obj,requester_role):
        self.search_helper=ConnectionSearchHelper(conds,requester_obj,requester_role)
        
    ##############################################
    def applyConditions(self):
        """
            Apply conditions on tables, should check conditions here
        """
        BaseConnectionLogSearcher.applyConditions(self)
        
        con_details_table=self.search_helper.getTable("connection_log_details")

        con_details_table.exactSearch(self.search_helper, "username", "username", MultiStr)
        con_details_table.exactSearch(self.search_helper, "voip_username", "voip_username", MultiStr)

        con_details_table.exactSearch(self.search_helper, "mac", "mac", MultiStr)
        con_details_table.exactSearch(self.search_helper, "caller_id", "caller_id", MultiStr)

        con_details_table.exactSearch(self.search_helper, "remote_ip", "remote_ip", MultiStr)
        con_details_table.exactSearch(self.search_helper, "station_ip", "station_ip", MultiStr)
              
    #################################################
    def getConnectionLog(self,_from,to,order_by,desc,date_type):
        """
            if total_credit or total_duration is smaller thatn 0, then it was not requested by caller, so we didn't
                calculate em
        """
        
        self.__getConnectionLogCheckInput(_from,to,order_by,desc)
        self.applyConditions()
        (total_rows,total_credit,total_duration,total_in,total_out,report)=self.search_helper.getConnectionLogs(_from,to,order_by,desc,date_type)
        return {"total_rows":total_rows,
                "total_credit":total_credit,
                "total_duration":total_duration,
                "total_in_bytes":float(total_in),
                "total_out_bytes":float(total_out),
                "report":report
               }

    def __getConnectionLogCheckInput(self,_from,to,order_by,desc):
        report_lib.checkFromTo(_from,to)
        self.__checkOrderBy(order_by)
        
    def __checkOrderBy(self,order_by):
        if order_by not in ["user_id","credit_used","login_time","logout_time","successful","service","ras_id"]:
            raise GeneralException(errorText("GENERAL","INVALID_ORDER_BY")%order_by)
            

    #########################################################
    def getDurations(self):
        #duration analysis implies successful calls
        self.search_helper.setCondValue("successful","yes")
        self.applyConditions()
        return self.search_helper.getDurations()

    def getGroupUsages(self):
        self.applyConditions()
        return self.search_helper.getGroupUsages()

    def getRasUsages(self):
        self.applyConditions()
        return self.search_helper.getRasUsages()

    def getAdminUsages(self):
        self.applyConditions()
        return self.search_helper.getAdminUsages()

    def getVoIPDisconnectCauses(self):
        self.applyConditions()
        return self.search_helper.getVoIPDisconnectCauses()

    def getSuccessfulCounts(self):
        self.applyConditions()
        return self.search_helper.getSuccessfulCounts()



_comment="""
IBSng=# EXPLAIN ANALYZE select * from connection_log where user_id in (select user_id from users where owner_id=0 or owner_id=1) order by login_time;
                                                     QUERY PLAN
---------------------------------------------------------------------------------------------------------------------
 Sort  (cost=2.23..2.23 rows=1 width=44) (actual time=0.173..0.189 rows=9 loops=1)
   Sort Key: connection_log.login_time
   ->  Nested Loop  (cost=1.02..2.22 rows=1 width=44) (actual time=0.053..0.139 rows=9 loops=1)
         Join Filter: ("inner".user_id = "outer".user_id)
         ->  HashAggregate  (cost=1.02..1.02 rows=1 width=8) (actual time=0.033..0.035 rows=1 loops=1)
               ->  Seq Scan on users  (cost=0.00..1.01 rows=1 width=8) (actual time=0.015..0.018 rows=1 loops=1)
                     Filter: ((owner_id = 0) OR (owner_id = 1))
         ->  Seq Scan on connection_log  (cost=0.00..1.09 rows=9 width=44) (actual time=0.005..0.030 rows=9 loops=1)
 Total runtime: 0.298 ms
(9 rows)

IBSng=# EXPLAIN ANALYZE select * from connection_log where exists (select users.user_id from users where users.user_id=connection_log.user_id and (users.owner_id=0 or owner_id=1)) order by login_time;
                                                   QUERY PLAN
----------------------------------------------------------------------------------------------------------------
 Sort  (cost=10.31..10.32 rows=5 width=44) (actual time=0.200..0.216 rows=9 loops=1)
   Sort Key: login_time
   ->  Seq Scan on connection_log  (cost=0.00..10.25 rows=5 width=44) (actual time=0.053..0.159 rows=9 loops=1)
         Filter: (subplan)
         SubPlan
           ->  Seq Scan on users  (cost=0.00..1.02 rows=1 width=8) (actual time=0.006..0.006 rows=1 loops=9)
                 Filter: ((user_id = $0) AND ((owner_id = 0) OR (owner_id = 1)))
 Total runtime: 0.296 ms
(8 rows)

"""