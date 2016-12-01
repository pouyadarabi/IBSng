from core.report.search_helper import SearchHelper
from core.report.search_table import SearchTable,SearchAttrsTable
from core.report.search_group import SearchGroup
from core.lib.multi_strs import MultiStr
from core.lib import report_lib
from core.lib.date import AbsDate
from core.admin import admin_main
from core.user import user_main
from core.ras import ras_main
from core.ibs_exceptions import *
from core.errors import errorText
from core.db import db_main
import types

class CreditChangeSearchTable(SearchTable):
    def __init__(self):
        SearchTable.__init__(self,"credit_change")
        
    def createQuery(self):
        if not self.getRootGroup().isEmpty():
            table_name=self.getTableName()
            return "select credit_change_id from %s where %s"%(table_name,self.getRootGroup().getConditionalClause())

class CreditChangeUserIDSearchTable(SearchTable):
    def __init__(self):
        SearchTable.__init__(self,"credit_change_userid")
        
    def createQuery(self):
        if not self.getRootGroup().isEmpty():
            table_name=self.getTableName()
            return "select distinct credit_change_id from %s where %s"%(table_name,self.getRootGroup().getConditionalClause())
        

class CreditSearchHelper(SearchHelper):
    def __init__(self,conds,requester_obj,requester_role):
        SearchHelper.__init__(self,conds,requester_obj,requester_role,
                                                    {"credit_change":CreditChangeSearchTable(),
                                                    "credit_change_userid":CreditChangeUserIDSearchTable()})
    def getCreditChanges(self,_from,to,order_by,desc,date_type):
        db_handle=db_main.getHandle(True)
        try:
            self.__createTempTable(db_handle)
            total_rows=self.__getTotalResultsCount(db_handle)
            if total_rows==0:
                return (0,0,0,[])
            total_per_user_credit=self.__getTotalPerUserCredit(db_handle)
            total_admin_credit=self.__getTotalAdminCredit(db_handle)
            credit_changes=self.__getCreditChanges(db_handle,_from,to,order_by,desc)
            user_ids=self.__getUserIDs(db_handle,credit_changes)
        finally:
            self.dropTempTable(db_handle,"credit_change_report")
            db_handle.releaseHandle()
            
        return (total_rows,total_per_user_credit,total_admin_credit,self.__createReportResult(credit_changes,user_ids,date_type))

    def __createReportResult(self,credit_changes,user_ids,date_type):
        user_ids=self.__convertUserIDsToDic(user_ids)
        self.__repairCreditChangeDic(credit_changes,user_ids,date_type)
        return credit_changes
        
    def __repairCreditChangeDic(self,credit_changes,user_ids,date_type):
        for change in credit_changes:
            change["change_time_formatted"]=AbsDate(change["change_time"],"gregorian").getDate(date_type)
            change["admin_name"]=admin_main.getLoader().getAdminByID(change["admin_id"]).getUsername()
            change["action_text"]=user_main.getCreditChangeLogActions().getIDActionText(change["action"])
            try:
                change["user_ids"]=user_ids[change["credit_change_id"]] 
            except KeyError:
                change["user_ids"]=[]
    
        return credit_changes
        
    def __convertUserIDsToDic(self,user_ids):
        """
            convert user ids to dic in format {credit_change_id:list of user_ids}
        """
        dic={}
        last_id=None
        for row in user_ids:
            if last_id!=row["credit_change_id"]:
                if last_id!=None:
                    dic[last_id]=per_change_list
                last_id=row["credit_change_id"]
                per_change_list=[]
            per_change_list.append(row["user_id"])

        if last_id!=None:
            dic[last_id]=per_change_list

        return dic
                
    def __getUserIDs(self,db_handle,credit_changes):
        credit_change_id_conds=map(lambda x:"credit_change_id=%s"%x["credit_change_id"],credit_changes)
        return db_handle.get("credit_change_userid",
                             " or ".join(map(lambda x:"%s::bigint"%x,credit_change_id_conds)),
                             0,-1,"credit_change_id,user_id asc")

    def __getCreditChanges(self,db_handle,_from,to,order_by,desc):
        return db_handle.get("credit_change_report,credit_change",
                             "credit_change.credit_change_id=credit_change_report.credit_change_id",
                             _from,
                             to,
                             (order_by,desc))
                      
    def __createTempTable(self,db_handle):
        select_query=self.__createCreditChangeIDsQuery()
        self.createTempTableAsQuery(db_handle,"credit_change_report",select_query)

    def __getTotalResultsCount(self,db_handle):
        return db_handle.getCount("credit_change_report","true")

    def __getTotalPerUserCredit(self,db_handle):
        if self.hasCondFor("show_total_per_user_credit"):
            return db_handle.selectQuery("select sum(per_user_credit) as sum from credit_change,credit_change_report where \
                                          credit_change.credit_change_id=credit_change_report.credit_change_id")[0]["sum"]
        return -1

    def __getTotalAdminCredit(self,db_handle):
        if self.hasCondFor("show_total_admin_credit"):
            return db_handle.selectQuery("select sum(admin_credit) as sum from credit_change,credit_change_report where \
                                          credit_change.credit_change_id=credit_change_report.credit_change_id")[0]["sum"]
        return -1
    
    def __createCreditChangeIDsQuery(self):
        queries=self.getTableQueries()
        queries=apply(self.filterNoneQueries,queries.values())
        if len(queries)==0:
            query="select credit_change_id from credit_change"
        else:
            query=self.intersectQueries(queries)
        return query

class CreditSearcher:
    def __init__(self,conds,requester_obj,requester_role):
        self.search_helper=CreditSearchHelper(conds,requester_obj,requester_role)
        
    ##############################################
    def applyConditions(self):
        """
            Apply conditions on tables, should check conditions here
        """
        credit_table=self.search_helper.getTable("credit_change")
        userid_table=self.search_helper.getTable("credit_change_userid")

        self.__addUserIDAndAdminCondition()

        credit_table.exactSearch(self.search_helper,"action","action",lambda action:user_main.getCreditChangeLogActions().getActionID(action))

        credit_table.ltgtSearch(self.search_helper,"per_user_credit","per_user_credit_op","per_user_credit")

        credit_table.ltgtSearch(self.search_helper,"admin_credit","admin_credit_op","admin_credit")

        self.search_helper.setCondValue("change_time_from_op",">=")     
        credit_table.dateSearch(self.search_helper,"change_time_from","change_time_from_unit","change_time_from_op","change_time")

        self.search_helper.setCondValue("change_time_to_op","<")
        credit_table.dateSearch(self.search_helper,"change_time_to","change_time_to_unit","change_time_to_op","change_time")

        credit_table.exactSearch(self.search_helper,"remote_addr","remote_addr",MultiStr)

    def __addUserIDAndAdminCondition(self):
        if self.search_helper.isRequesterAdmin():
            admin_restricted=not self.search_helper.getRequesterObj().isGod() and self.search_helper.getRequesterObj().getPerms()["SEE CREDIT CHANGES"].isRestricted()
            if admin_restricted:
                admin_id = self.search_helper.getRequesterObj().getAdminID()
#               self.search_helper.getTable("credit_change").getRootGroup().addGroup("admin_id=%s"%admin_id)
                sub_query=self.__userOwnersConditionQuery(admin_id)
                self.search_helper.getTable("credit_change_userid").getRootGroup().addGroup(sub_query)      
            else:
                self.search_helper.getTable("credit_change").exactSearch(self.search_helper,"admin","admin_id",lambda admin_username:admin_main.getLoader().getAdminByName(admin_username).getAdminID())
            
        self.search_helper.getTable("credit_change_userid").exactSearch(self.search_helper,"user_ids","user_id",MultiStr)

    def __userOwnersConditionQuery(self,admin_id):
        return "credit_change_userid.user_id in (select user_id from users where owner_id=%s)"%admin_id
        
    #################################################
    def getCreditChanges(self,_from,to,order_by,desc,date_type):
        """
            return a list of credit changes
        """
        self.__getCreditChangesCheckInput(_from,to,order_by,desc)
        self.applyConditions()
        (total_rows,total_per_user_credit,total_admin_credit,report)=self.search_helper.getCreditChanges(_from,to,order_by,desc,date_type)
        return {"total_rows":total_rows,
                "total_per_user_credit":total_per_user_credit,
                "total_admin_credit":total_admin_credit,
                "report":report
               }

    def __getCreditChangesCheckInput(self,_from,to,order_by,desc):
        report_lib.checkFromTo(_from,to)
        self.__checkOrderBy(order_by)
        
    def __checkOrderBy(self,order_by):
        if order_by not in ["change_time","per_user_credit","admin_credit"]:
            raise GeneralException(errorText("GENERAL","INVALID_ORDER_BY")%order_by)
