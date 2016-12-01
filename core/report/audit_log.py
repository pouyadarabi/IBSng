from core.report.search_helper import SearchHelper
from core.report.search_table import SearchTable
from core.report.search_group import SearchGroup
from core.lib.multi_strs import MultiStr
from core.lib import report_lib
from core.lib.date import AbsDate
from core.admin import admin_main
from core.group import group_main
from core.user import user_main
from core.ibs_exceptions import *
from core.errors import errorText
from core.db import db_main
import types

class UserAuditSearchTable(SearchTable):
    def __init__(self):
        SearchTable.__init__(self,"user_audit_log")
        
class UserAuditSearchHelper(SearchHelper):
    def __init__(self,conds,requester_obj,requester_role):
        SearchHelper.__init__(self,conds,requester_obj,requester_role,
                                                    {"user_audit_log":UserAuditSearchTable()})

    def getUserAuditLogs(self,_from,to,order_by,desc,date_type):
        cond = self.getTable("user_audit_log").getRootGroup().getConditionalClause()
        result = self.__getResult(cond, _from, to, order_by, desc)
        total_rows = self.__getTotalResultsCount(cond)
        return (total_rows, self.__createReportResult(result, date_type) )


    def __getResult(self, cond, _from, to, order_by, desc):
        return db_main.getHandle().get("user_audit_log",cond,_from,to,(order_by,desc))

    def __getTotalResultsCount(self, cond):
        return db_main.getHandle().getCount("user_audit_log",cond)

    def __createReportResult(self,result,date_type):
        for row in result:
            row["change_time_formatted"] = AbsDate(row["change_time"],"gregorian").getDate(date_type)
            row["admin_name"] = admin_main.getLoader().getAdminByID(row["admin_id"]).getUsername()
            if row["is_user"] == "t":
                row["username"] = user_main.getActionManager().getUsernameReprForUserID(row["object_id"])
            else:
                row["group_name"] = group_main.getLoader().getGroupByID(row["object_id"]).getGroupName()

        return result

class UserAuditLogSearcher:
    def __init__(self,conds,requester_obj,requester_role):
        self.search_helper=UserAuditSearchHelper(conds,requester_obj,requester_role)
        
    ##############################################
    def applyConditions(self):
        """
            Apply conditions on tables, should check conditions here
        """
        user_audit_table = self.search_helper.getTable("user_audit_log")

        self.__addAdminCondition(user_audit_table)

        if self.search_helper.hasCondFor("user_ids"):
            if self.search_helper.getCondValue("user_ids") != "":
                user_audit_table.exactSearch(self.search_helper,"user_ids","object_id",MultiStr)

            user_audit_table.getRootGroup().addGroup("is_user = 't'")
        
        if self.search_helper.hasCondFor("group_name"):
            if self.search_helper.getCondValue("group_name") != "":
                user_audit_table.exactSearch(self.search_helper,"group_name","object_id",lambda group_name:group_main.getLoader().getGroupByName(group_name).getGroupID())
                
            user_audit_table.getRootGroup().addGroup("is_user = 'f'")

        user_audit_table.exactSearch(self.search_helper,"attr_names","attr_name",MultiStr)

        self.search_helper.setCondValue("change_time_from_op",">=")     
        user_audit_table.dateSearch(self.search_helper,"change_time_from","change_time_from_unit","change_time_from_op","change_time")

        self.search_helper.setCondValue("change_time_to_op","<")
        user_audit_table.dateSearch(self.search_helper,"change_time_to","change_time_to_unit","change_time_to_op","change_time")


    def __addAdminCondition(self, user_audit_table):
        if self.search_helper.isRequesterAdmin():
            admin_restricted=not self.search_helper.getRequesterObj().isGod() and self.search_helper.getRequesterObj().getPerms()["SEE USER AUDIT LOGS"].isRestricted()
            if admin_restricted:
                user_audit_table.getRootGroup().addGroup("admin_id=%s"%self.search_helper.getRequesterObj().getAdminID())
            else:
                user_audit_table.exactSearch(self.search_helper,"admin","admin_id",lambda admin_username:admin_main.getLoader().getAdminByName(admin_username).getAdminID())
            
    #################################################
    def getUserAuditLogs(self,_from,to,order_by,desc,date_type):
        """
            return a dic of user audit logs
        """
        self.__getUserAuditLogsCheckInput(_from,to,order_by,desc)
        self.applyConditions()
        (total_rows, report)=self.search_helper.getUserAuditLogs(_from,to,order_by,desc,date_type)
        return {"total_rows":total_rows,
                "report":report}

    def __getUserAuditLogsCheckInput(self,_from,to,order_by,desc):
        report_lib.checkFromTo(_from,to)
        self.__checkOrderBy(order_by)
        
    def __checkOrderBy(self,order_by):
        if order_by not in ["change_time","object_id","admin_id"]:
            raise GeneralException(errorText("GENERAL","INVALID_ORDER_BY")%order_by)
