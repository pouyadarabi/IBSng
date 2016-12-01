from core.user import user_main
from core.lib import report_lib
from core.db import db_main
from core.report.search_helper import SearchHelper
from core.report.connection import ConnectionLogSearchTable, BaseConnectionLogSearcher

class ConnectionUsageSearchHelper(SearchHelper):
    def __init__(self,conds,requester_obj,requester_role):
        SearchHelper.__init__(self,conds,requester_obj,requester_role,
                                                     {"connection_log":ConnectionLogSearchTable()})

    ############################################
    def getInOutUsages(self,_from,to):
        """
            return a dic in format {"total_rows":,"report":[[user_id, user_repr, in_usage, out_usage]]}. 
            The report list is sorted by in_usage 
        """
        conditions = self.getTable("connection_log").getRootGroup().getConditionalClause()
        if conditions == "":
            conditions = " true "

        total_rows = self.__getInOutUsageTotalRows(conditions)
        if total_rows == 0:
            return {"report":[], "total_rows":0}
        
        in_usages = self.__getInUsages(conditions, _from, to)
        out_usages = self.__getOutUsages(conditions, in_usages)
        
        return {"report":self.__createInOutUsageReportList(in_usages, out_usages),
                "total_rows":total_rows}
        
    def __getInOutUsageTotalRows(self, conditions):
        """
            find total rows just by checking unique user ids that has connection log with at least on
            "bytes_in" in details
        """
        total_rows_query = "select count(distinct user_id) as count from connection_log where " + \
                            "%s and "%conditions + \
                            "connection_log_id in " + \
                            "(select connection_log_details.connection_log_id from connection_log_details where connection_log_details.name = 'bytes_in')"
        
        return db_main.getHandle().selectQuery(total_rows_query)[0]["count"]
    
    def __getInUsages(self, conditions, _from, to):
        in_usage_query = "select user_id, sum(value::bigint) as sum " + \
                            "from connection_log_details,connection_log " + \
                            "where %s and "%conditions + \
                            "name='bytes_in' and " + \
                            "connection_log.connection_log_id=connection_log_details.connection_log_id " + \
                            "group by user_id order by sum(value::bigint) desc offset %s limit %s"%(_from, to-_from)
        return db_main.getHandle().selectQuery(in_usage_query, 1) #tuple result
    
    def __getOutUsages(self, conditions, in_usages):
        user_ids = [_tuple[0] for _tuple in in_usages]
        user_id_condition = ",".join(map(str, user_ids)) 
        
        out_usage_query = "select user_id, sum(value::bigint) as sum " + \
                            "from connection_log_details,connection_log " + \
                            "where %s and "%conditions + \
                            "name='bytes_out' and user_id in (%s) and "%user_id_condition + \
                            "connection_log.connection_log_id=connection_log_details.connection_log_id " + \
                            "group by user_id"
        return db_main.getHandle().selectQuery(out_usage_query, 1) #tuple result
    
    def __createInOutUsageReportList(self, in_usages, out_usages):
        """
            merge in_usages and out_usages and return a list in format [[user_id, user_repr, in_usage, out_usage],..]
        """
        out_usage_dic = {}
        for user_id, out_usage in out_usages:
            out_usage_dic[user_id] = out_usage
        
        inout_usage = []
        for user_id, in_usage in in_usages:
            inout_usage.append([user_id, 
                                user_main.getActionManager().getUsernameReprForUserID(user_id),
                                in_usage, 
                                out_usage_dic[user_id]])
        
        return inout_usage

    ###########################################
    def __getUniqueUserIDs(self, conditions):
        """
            return total number of unique user_ids with "conditions" in connection_log
        """
        total_rows_query = "select count(distinct user_id) as count from connection_log where " + conditions
        return db_main.getHandle().selectQuery(total_rows_query)[0]["count"]

    def __getGroupByUserIDSum(self, column, conditions, _from, to):
        query = "select user_id, sum(%s) as sum from connection_log where %s group by user_id order by sum desc offset %s limit %s"% \
                    (column, conditions, _from, to - _from)
        
        return db_main.getHandle().selectQuery(query, 1)

    def __addUsernameRepr(self, report):
        fixed_report = []
        
        for user_id, value in report:
            fixed_report.append([user_id,
                                 user_main.getActionManager().getUsernameReprForUserID(user_id),
                                 value])
        
        return fixed_report
    
    def __getUsageReport(self, column, _from, to):
        """
            Do a group by user query with sum of "column" and return the results
            
            return value is a dic in format {"total_rows":,"report":[[user_id, user_repr, value]]}. 
            The report list is sorted by value 
        """

        conditions = self.getTable("connection_log").getRootGroup().getConditionalClause()
        if conditions == "":
            conditions = " true "

        total_rows = self.__getUniqueUserIDs(conditions)
        if total_rows == 0:
            return {"report":[], "total_rows":0}
        
        db_report = self.__getGroupByUserIDSum(column, conditions, _from, to)
        return {"report":self.__addUsernameRepr(db_report),
                "total_rows":total_rows}
        
    ###########################################        
    def getCreditUsages(self,_from,to):
        """
            return a dic in format {"total_rows":,"report":[[user_id, user_repr, credit_usage]]}. 
            The report list is sorted by credit 
        """
        return self.__getUsageReport("credit_used", _from, to)
        
    ############################################
    def getDurationUsages(self,_from,to):
        """
            return a dic in format {"total_rows":,"report":[[user_id, user_repr, duration_second_usage]]}. 
            The report list is sorted by duration_second_usage
        """
        return self.__getUsageReport("extract(epoch from logout_time - login_time)", _from, to)

class ConnectionUsageSearcher(BaseConnectionLogSearcher):
    def __init__(self,conds,requester_obj,requester_role):
        self.search_helper=ConnectionUsageSearchHelper(conds,requester_obj,requester_role)

    def __checkInput(self,_from,to):
        report_lib.checkFromTo(_from,to)
    
    def getInOutUsages(self, _from, to):
        self.__checkInput(_from, to)
        self.applyConditions()
        return self.search_helper.getInOutUsages(_from, to)

    def getCreditUsages(self, _from, to):
        self.__checkInput(_from, to)
        self.applyConditions()
        return self.search_helper.getCreditUsages(_from, to)

    def getDurationUsages(self, _from, to):
        self.__checkInput(_from, to)
        self.applyConditions()
        return self.search_helper.getDurationUsages(_from, to)
