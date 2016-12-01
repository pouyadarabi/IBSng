from core.report.search_helper import SearchHelper
from core.report.search_table import SearchTable
from core.report.search_group import SearchGroup
from core.user import user_main
from core.db import db_main
#from core.db import ibs_query
from core.lib.general import *
from core.lib import report_lib
from core.lib.multi_strs import MultiStr
from core.lib.date import *

class WebAnalyzerSearchTable(SearchTable):
    def __init__(self):
        SearchTable.__init__(self,"web_analyzer_log")
        

class WebAnalyzerSearchHelper(SearchHelper):
    def __init__(self,conds,requester_obj,requester_role):
        SearchHelper.__init__(self,conds,requester_obj,requester_role,
                                                    {"web_analyzer_log":WebAnalyzerSearchTable()})

    def getWebAnalyzerLogs(self,_from,to,order_by,desc,date_type):
        cond = self.getTable("web_analyzer_log").getRootGroup().getConditionalClause()
        result = self.__getResult(cond, _from, to, order_by, desc)

        totals = self.__getTotals(cond)

        return (totals,
                self.__createReportResult(result, date_type) )
    
    
    def getTopVisited(self, _from, to, date_type):
        cond = self.getTable("web_analyzer_log").getRootGroup().getConditionalClause()
        top_visited = self.__getTopVisited(cond, _from, to)
        total_count = self.__getTotalCount("web_analyzer_log", cond)
        
        return (top_visited, total_count)
        
    
    def __getTopVisited(self, cond, _from, to):
        cond += " group by (url)"
        return db_main.getHandle().get("web_analyzer_log", cond, _from, to, "sum(_count) desc",
                                         ["url", "sum(_count) as count"])

    def __getTotalCount(self, table_name, cond):
        return db_main.getHandle().getCount(table_name,cond)
    
    def __getResult(self, cond, _from, to, order_by, desc):
        return db_main.getHandle().get("web_analyzer_log left join normal_users using (user_id)",cond,_from,to,(order_by,desc),
                                        ["web_analyzer_log.*","normal_users.normal_username as username"])

    def __getTotals(self, cond):
        db_totals = db_main.getHandle().get("web_analyzer_log", cond, 0, -1, "", ["count(*) as total_rows",
                                                                             "sum(_count) as total_count",
                                                                             "sum(elapsed) as total_elapsed",
                                                                             "sum(bytes) as total_bytes",
                                                                             "sum(miss) as total_miss",
                                                                             "sum(hit) as total_hit",
                                                                             "sum(successful) as total_success",
                                                                             "sum(failure) as total_failure"
                                                                            ])[0]

        return self.__noneToZero(db_totals)

    def __noneToZero(self, _dic):
        """
            convert all None values in _dic to zero
        """
        for key in _dic:
            if _dic[key]==None:
                _dic[key]=0
            else:
                _dic[key] = float(_dic[key])
        return _dic
        

    def __createReportResult(self, result, date_type):
        for row in result:
            row["date_formatted"]=AbsDate(row["_date"],"gregorian").getDate(date_type)
            if row["username"] == None:
                row["username"] = "N/A"
        return result


class WebAnalyzerSearcher:
    def __init__(self, conds, requester_obj, requester_role):
        self.search_helper=WebAnalyzerSearchHelper(conds, requester_obj, requester_role)
        
    ##############################################
    def applyConditions(self):
        """
            Apply conditions on tables, should check conditions here
        """
        web_analyzer_table = self.search_helper.getTable("web_analyzer_log")

        web_analyzer_table.ltgtSearch(self.search_helper, "log_id", "log_id_op", "log_id", lambda x:to_int(x,"log id"))

        self.search_helper.setCondValue("date_from_op",">=")    
        web_analyzer_table.dateSearch(self.search_helper,"date_from","date_from_unit","date_from_op","_date")
        
        self.search_helper.setCondValue("date_to_op","<")
        web_analyzer_table.dateSearch(self.search_helper,"date_to","date_to_unit","date_to_op","_date")

        self.__addUserIDCondition(web_analyzer_table)

        web_analyzer_table.exactSearch(self.search_helper,"ip_addr","ip_addr")
        web_analyzer_table.likeStrSearch(self.search_helper,"url","url_op","url")
        
        web_analyzer_table.ltgtSearch(self.search_helper, "elapsed", "elapsed_op", "elapsed", lambda x:to_int(x,"elapsed"))
        web_analyzer_table.ltgtSearch(self.search_helper, "bytes", "bytes_op", "bytes", lambda x:to_int(x,"bytes"))
        
    def __addUserIDCondition(self, web_analyzer_table):
        if self.search_helper.isRequesterAdmin():
            admin_restricted=not self.search_helper.getRequesterObj().isGod() and self.search_helper.getRequesterObj().getPerms()["SEE WEB ANALYZER LOGS"].isRestricted()
            if admin_restricted or self.search_helper.hasCondFor("owner"):
                if admin_restricted:
                    owner_ids=(self.search_helper.getRequesterObj().getAdminID(),)
                else:
                    owner_name=self.search_helper.getCondValue("owner")
                    if type(owner_name)==types.StringType:
                        owner_name=(owner_name,)
                    owner_ids=map(lambda owner_name:admin_main.getLoader().getAdminByName(owner_name).getAdminID(),owner_name)
            
                sub_query=self.__userOwnersConditionQuery(owner_ids)
                web_analyzer_table.getRootGroup().addGroup(sub_query)
        
        web_analyzer_table.exactSearch(self.search_helper,"user_ids","user_id",MultiStr)        

    def __userOwnersConditionQuery(self,owner_ids):
        cond_group=SearchGroup("or")
        map(lambda owner_id:cond_group.addGroup("users.owner_id=%s"%owner_id),owner_ids)
        return "web_analyzer_log.user_id in (select user_id from users where %s)"%cond_group.getConditionalClause()

    #################################################
    def getWebAnalyzerLogs(self, _from, to, order_by, desc, date_type):
        """
            return a list of user audit logs (totals,result)

            totals contains:
            
                totals["total_rows"], 
                totals["total_count"],
                totals["total_elpased"],
                totals["total_bytes"],
                totals["total_miss"],
                totals["total_hit"],
                totals["total_success"],
                totals["total_failure"],            
        """
        self.__webAnalyzerLogsCheckInput(_from, to, order_by, desc)
        self.applyConditions()
        (totals, report) = self.search_helper.getWebAnalyzerLogs(_from, to, order_by, desc, date_type)
        return (totals, report)


    def getTopVisited(self, _from, to, date_type):
        self.__topVisitedCheckInput(_from, to)
        self.applyConditions()
        return self.search_helper.getTopVisited(_from, to, date_type)

    def __topVisitedCheckInput(self, _from , to):
        report_lib.checkFromTo(_from, to)
    
    def __webAnalyzerLogsCheckInput(self, _from, to, order_by, desc):
        report_lib.checkFromTo(_from, to)
        self.__checkOrderBy(order_by)
        
    def __checkOrderBy(self,order_by):
        if order_by not in ["log_id","_date","user_id"]:
            raise GeneralException(errorText("GENERAL","INVALID_ORDER_BY")%order_by)
