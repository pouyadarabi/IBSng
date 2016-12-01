from core.report.search_helper import SearchHelper
from core.report.search_table import SearchTable
from core.report.search_group import SearchGroup
from core.lib import report_lib
from core.lib.date import AbsDate
from core.admin import admin_main
from core.group import group_main
from core.user import user_main
from core.ibs_exceptions import *
from core.errors import errorText
from core.db import db_main
import types

class AdminDepositChangeLogsSearchTable(SearchTable):
    def __init__(self):
        SearchTable.__init__(self,"admin_deposit_change")
        
class AdminDepositChangeLogsSearchHelper(SearchHelper):
    def __init__(self,conds,requester_obj,requester_role):
        SearchHelper.__init__(self,conds,requester_obj,requester_role,
                                                    {"admin_deposit_change":AdminDepositChangeLogsSearchTable()})

    def getAdminDepositChangeLogs(self,_from,to,order_by,desc,date_type):
        cond = self.getTable("admin_deposit_change").getRootGroup().getConditionalClause()
        total_rows = self.__getTotalResultsCount(cond)

	if total_rows == 0:
	    return (0, 0, [])

        result = self.__getResult(cond, _from, to, order_by, desc)
        if self.hasCondFor("show_total_deposit_change"):
            total_change_deposit = self.__getTotalDepositChangeSum(cond, _from, to)
        else:
    	    total_change_deposit = 0
    	    
        return (total_rows, total_change_deposit, self.__createReportResult(result, date_type))


    def __getResult(self, cond, _from, to, order_by, desc):
        return db_main.getHandle().get("admin_deposit_change",cond,_from,to,(order_by,desc))

    def __getTotalResultsCount(self, cond):
        return db_main.getHandle().getCount("admin_deposit_change",cond)

    def __getTotalDepositChangeSum(self, cond, _from, to):
        return db_main.getHandle().get("admin_deposit_change",cond,0,-1,"", ["sum(deposit_change) as sum"])[0]["sum"]

    def __createReportResult(self,result,date_type):
        for row in result:
            row["change_time_formatted"] = AbsDate(row["change_time"],"gregorian").getDate(date_type)
            row["from_admin_name"] = admin_main.getLoader().getAdminByID(row["admin_id"]).getUsername()
            row["to_admin_name"] = admin_main.getLoader().getAdminByID(row["to_admin_id"]).getUsername()

        return result

class AdminDepositChangeLogsSearcher:
    def __init__(self,conds,requester_obj,requester_role):
        self.search_helper=AdminDepositChangeLogsSearchHelper(conds,requester_obj,requester_role)
        
    ##############################################
    def applyConditions(self):
        """
            Apply conditions on tables, should check conditions here
        """
        deposit_change_table = self.search_helper.getTable("admin_deposit_change")

        deposit_change_table.exactSearch(self.search_helper,"from_admin","admin_id",
             lambda owner_name:admin_main.getLoader().getAdminByName(owner_name).getAdminID())

        deposit_change_table.exactSearch(self.search_helper,"to_admin","to_admin_id",
             lambda owner_name:admin_main.getLoader().getAdminByName(owner_name).getAdminID())
        
        self.search_helper.setCondValue("change_time_from_op",">=")  
        deposit_change_table.dateSearch(self.search_helper,"change_time_from","change_time_from_unit","change_time_from_op","change_time")

        self.search_helper.setCondValue("change_time_to_op","<") 
        deposit_change_table.dateSearch(self.search_helper,"change_time_to" ,"change_time_to_unit","change_time_to_op","change_time")

    #################################################
    def getAdminDepositChangeLogs(self,_from,to,order_by,desc,date_type):
        """
            return a dic of user audit logs
        """
        self.__getAdminDepositChangeLogsCheckInput(_from,to,order_by,desc)
        self.applyConditions()
        (total_rows, total_change_deposit, report)=self.search_helper.getAdminDepositChangeLogs(_from,to,order_by,desc,date_type)
        return {"total_rows":total_rows,
                "total_deposit_change":total_change_deposit,
                "report":report}

    def __getAdminDepositChangeLogsCheckInput(self,_from,to,order_by,desc):
        report_lib.checkFromTo(_from,to)
        self.__checkOrderBy(order_by)
        
    def __checkOrderBy(self,order_by):
        if order_by not in ["admin_id", "to_admin_id", "change_time", "deposit_change"]:
            raise GeneralException(errorText("GENERAL","INVALID_ORDER_BY")%order_by)
