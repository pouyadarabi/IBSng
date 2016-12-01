from core.report.search_helper import SearchHelper
from core.report.search_table import SearchTable
from core.lib.multi_strs import MultiStr
from core.user import user_main
from core.lib import report_lib
from core.lib.date import AbsDate
from core.db import db_main

from core.ibs_exceptions import *
from core.errors import errorText

class AdminMessagesSearchTable(SearchTable):
    def __init__(self):
        SearchTable.__init__(self,"admin_messages")

class UserMessagesSearchTable(SearchTable):
    def __init__(self):
        SearchTable.__init__(self,"user_messages")
        
class MessagesSearchHelper(SearchHelper):
    def __init__(self,conds,requester_obj,requester_role, table_name, table_obj):
        SearchHelper.__init__(self,conds,requester_obj,requester_role,
                                                    {table_name:table_obj})
        self.table_name = table_name

    def getMessages(self, _from, to, order_by, desc, date_type):
        cond = self.getTable(self.table_name).getRootGroup().getConditionalClause()
        result = self.__getResult(cond, _from, to, order_by, desc)
        total_rows = self.__getTotalResultsCount(cond)
        return (total_rows, self.__createReportResult(result, date_type) )

    def __getResult(self, cond, _from, to, order_by, desc):
        return db_main.getHandle().get(self.table_name, cond, _from, to, (order_by,desc))

    def __getTotalResultsCount(self, cond):
        return db_main.getHandle().getCount(self.table_name,cond)

    def __createReportResult(self,result,date_type):
        requester_is_admin = self.isRequesterAdmin()
        for row in result:
            row["post_date_formatted"]=AbsDate(row["post_date"],"gregorian").getDate(date_type)
            if row["user_id"]== None:
                row["user_id"]="ALL USERS"
                if requester_is_admin:
                    row["username_text"]="ALL USERS"
                
            elif requester_is_admin:
                row["username_text"]=user_main.getActionManager().getUsernameReprForUserID(row["user_id"])

        return result

class MessageSearcher:
    def __init__(self,conds,requester_obj,requester_role, table_name):
        if table_name == "admin_messages":
            table_obj = AdminMessagesSearchTable()
        else:
            table_obj = UserMessagesSearchTable()
            
        self.table_name = table_name
        self.search_helper=MessagesSearchHelper(conds,requester_obj,requester_role, table_name, table_obj)
        
    ##############################################
    def applyConditions(self):
        """
            Apply conditions on tables, should check conditions here
        """
        messages_table = self.search_helper.getTable(self.table_name)

        if self.search_helper.isRequesterAdmin():
            messages_table.exactSearch(self.search_helper,"user_ids","user_id",MultiStr)
        else:
            messages_table.getRootGroup().addGroup("user_id = %s or user_id is null"%self.search_helper.getRequesterObj().getUserID())
        
        messages_table.ltgtSearch(self.search_helper,"message_id","message_id_op","message_id")

        self.search_helper.setCondValue("post_date_from_op",">=")       
        messages_table.dateSearch(self.search_helper,"post_date_from","post_date_from_unit","post_date_from_op","post_date")

        self.search_helper.setCondValue("post_date_to_op","<")
        messages_table.dateSearch(self.search_helper,"post_date_to","post_date_to_unit","post_date_to_op","post_date")
            
    #################################################
    def getMessages(self,_from,to,order_by,desc,date_type):
        """
            return a list of messages {"messages":,"total_rows":}
        """
        self.__getMessagesCheckInput(_from,to,order_by,desc)
        self.applyConditions()
        (total_rows, messages)=self.search_helper.getMessages(_from,to,order_by,desc,date_type)
        return {"total_rows":total_rows,
                "messages":messages}

    def __getMessagesCheckInput(self,_from,to,order_by,desc):
        report_lib.checkFromTo(_from,to)
        self.__checkOrderBy(order_by)
        
    def __checkOrderBy(self,order_by):
        if order_by not in ["message_id","user_id","post_date"]:
            raise GeneralException(errorText("GENERAL","INVALID_ORDER_BY")%order_by)

