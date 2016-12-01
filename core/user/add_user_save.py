from core.lib.general import *
from core.ibs_exceptions import *
from core.errors import errorText
from core.report.search_helper import SearchHelper
from core.report.search_table import SearchTable,SearchAttrsTable
from core.admin import admin_main
from core.server import handler
from core.db import ibs_db,db_main
from core.lib import report_lib
from core.lib.multi_strs import MultiStr
from core.lib.date import AbsDate
from core.user import user_main

import itertools

class AddUserSaveActions:
    TYPES={"Normal":1,"VoIP":2}
    TYPES_REV={1:"Normal",2:"VoIP"}
    def newAddUser(self,ibs_query,user_ids,usernames,passwords,admin_id,_type,comment):
        """
            add new user add to keep in db.
            user_ids(list): list of user ids
            usernames(list or multistr): list of usernames that will be kept in this user add
            passwords(list of Password instances): list of passwords
            admin_id(integer): id of admin doing the add user
            _type(str): "Normal" or "VoIP"
            comment(str)
        """
        add_user_id=self.__getNewUserAddID()
        ibs_query+=self.__insertAddUserQuery(add_user_id,admin_id,self.getTypeID(_type),comment)
        ibs_query+=map(self.__insertAddUserDetailsQuery,
                       itertools.repeat(add_user_id,len(user_ids)),
                       user_ids,
                       usernames,
                       map(lambda x:x.getPassword(),passwords)
                       )
        return ibs_query

    def __getNewUserAddID(self):
        return db_main.getHandle().seqNextVal("users_user_id_seq")

    def __insertAddUserDetailsQuery(self,add_user_id,user_id,username,password):
        return ibs_db.createInsertQuery("add_user_save_details",{"add_user_save_id":add_user_id,
                                                                 "user_id":user_id,
                                                                 "username":dbText(username),
                                                                 "password":dbText(password)
                                                                })

    def __insertAddUserQuery(self,add_user_id,admin_id,type_id,comment):
        return ibs_db.createInsertQuery("add_user_saves",{"add_user_save_id":add_user_id,
                                                          "admin_id":admin_id,
                                                          "type":type_id,
                                                          "comment":dbText(comment)
                                                         })

    def getTypeID(self,_type):
        return self.TYPES[_type]

    def getIDTypeStr(self,_type_id):
        return self.TYPES_REV[_type_id]

    #########################################################
    def deleteAddUserSaves(self, add_user_save_ids, admin_obj):
        """
            add_user_save_id(list integer): add user save ids to be deleted
            admin_obj(obj): Admin Object of requester]
            
            This function take care of restricted permission too
        """
        admin_restricted=not admin_obj.isGod() and admin_obj.getPerms()["SEE SAVED USERNAME PASSWORDS"].isRestricted()
        self.__deleteAddUserSavesCheckInput(add_user_save_ids, admin_obj)       
        self.__deleteAddUserSavesDB(add_user_save_ids, admin_restricted, admin_obj)

    def __deleteAddUserSavesCheckInput(self, add_user_save_ids, admin_obj):
        for add_user_save_id in add_user_save_ids:
            if not isInt(add_user_save_id):
                raise GeneralException(errorText("USER_ACTIONS","INVALID_ADD_USER_SAVE_ID"))
        
    def __deleteAddUserSavesDB(self,add_user_save_ids, admin_restricted, admin_obj):
        query=""
        for add_user_save_id in add_user_save_ids:
            query += self.__deleteAddUserSaveQuery(add_user_save_id, admin_restricted, admin_obj.getAdminID())

        db_main.getHandle().transactionQuery(query)
        
    def __deleteAddUserSaveQuery(self, add_user_save_id, admin_restricted, admin_id):
        cond="add_user_save_id=%s"%add_user_save_id
        if admin_restricted:
            cond+=" and admin_id=%s"%admin_id
            details_cond="add_user_save_id in (select add_user_save_id from add_user_saves where %s)"%cond
        else:
            details_cond=cond    
            
        return ibs_db.createDeleteQuery("add_user_save_details",details_cond) + \
                ibs_db.createDeleteQuery("add_user_saves",details_cond)
        

class AddUserSaveHandler(handler.Handler):
    def __init__(self):    
        handler.Handler.__init__(self,"addUserSave")
        self.registerHandlerMethod("searchAddUserSaves")
        self.registerHandlerMethod("deleteAddUserSaves")

    def searchAddUserSaves(self,request):
        request.needAuthType(request.ADMIN)
        request.checkArgs("from","to","desc","order_by","conds")
        request.getAuthNameObj().canDo("SEE SAVED USERNAME PASSWORDS")
        searcher=AddUserSaveSearcher(request["conds"],request.getAuthNameObj())
        return searcher.getAddUserSaves(request["from"],request["to"],request["order_by"],request["desc"],request.getDateType())

    def deleteAddUserSaves(self,request):
        request.needAuthType(request.ADMIN)
        request.checkArgs("add_user_save_ids")
        request.getAuthNameObj().canDo("SEE SAVED USERNAME PASSWORDS")
        add_user_save_ids=map(lambda add_user_save_id:to_int(add_user_save_id,"add user save id"),request.fixList("add_user_save_ids"))
        user_main.getAddUserSaveActions().deleteAddUserSaves(add_user_save_ids,
                                                            request.getAuthNameObj())
        

class AddUserSaveSearchTable(SearchTable):
    def __init__(self):
        SearchTable.__init__(self,"add_user_saves")
        
    def createQuery(self):
        if not self.getRootGroup().isEmpty():
            table_name=self.getTableName()
            return "select add_user_save_id from %s where %s"%(table_name,self.getRootGroup().getConditionalClause())

class AddUserSaveDetailsSearchTable(SearchTable):
    def __init__(self):
        SearchTable.__init__(self,"add_user_save_details")
        
    def createQuery(self):
        if not self.getRootGroup().isEmpty():
            table_name=self.getTableName()
            return "select distinct add_user_save_id from %s where %s"%(table_name,self.getRootGroup().getConditionalClause())

class AddUserSaveSearchHelper(SearchHelper):
    def __init__(self,conds, admin_obj):
        SearchHelper.__init__(self, conds, admin_obj, "admin",
                                                    {"add_user_saves":AddUserSaveSearchTable(),
                                                    "add_user_save_details":AddUserSaveDetailsSearchTable()})

    def getAddUserSaves(self,_from,to,order_by,desc,date_type):
        """
            return (total_rows,list of results)
        """
        db_handle=db_main.getHandle(True)
        try:
            self.__createTempTable(db_handle)
            total_rows=self.__getTotalResultsCount(db_handle)
            if total_rows==0:
                return (0,[])
            add_user_saves=self.__getAddUserSaves(db_handle,_from,to,order_by,desc)
            users_from,users_to = self.__getUsersFromTo()
            details=self.__getAddUserSaveDetails(db_handle,add_user_saves,users_from,users_to)
            counts=self.__getUserCounts(db_handle, add_user_saves)
        finally:
            self.dropTempTable(db_handle,"add_user_save_report")
            db_handle.releaseHandle()
            
        return (total_rows,self.__createReportResult(add_user_saves,details,counts,date_type))

    ########################################
    def __getUsersFromTo(self):
        if self.hasCondFor("users_from","users_to"):
            return self.getCondValue("users_from"), self.getCondValue("users_to")
        else:
            return 0,-1

    def __createTempTable(self,db_handle):
        select_query=self.__createAddUserSaveIDsQuery()
        self.createTempTableAsQuery(db_handle,"add_user_save_report",select_query)

    def __createAddUserSaveIDsQuery(self):
        return self.createGetIDQuery("select add_user_save_id from add_user_saves")

    ##################################
    def __getTotalResultsCount(self,db_handle):
        return db_handle.getCount("add_user_save_report","true")

    ##################################  
    def __getAddUserSaves(self,db_handle,_from,to,order_by,desc):
        return db_handle.get("add_user_save_report,add_user_saves",
                             "add_user_saves.add_user_save_id=add_user_save_report.add_user_save_id",
                             _from,
                             to,
                             (order_by,desc))
    ###################################

    def __getAddUserSaveDetails(self,db_handle,add_user_saves,users_from,users_to):
        ret = {}
        for add_user_save in add_user_saves:
            ret[add_user_save["add_user_save_id"]] = db_handle.get("add_user_save_details",
                                                    "add_user_save_id=%s"%add_user_save["add_user_save_id"],
                                                    users_from,users_to,"user_id asc")
        return ret
    
    ###################################
    def __getUserCounts(self, db_handle, add_user_saves):
        if self.hasCondFor("get_counts"): #let's see if it's requested
            add_user_save_condition = self.__getAddUserSaveIDCondition(add_user_saves)
            db_counts = db_handle.selectQuery("select count(user_id) as count,add_user_save_id from add_user_save_details where %s group by add_user_save_id"%add_user_save_condition)
            ret = {}
            for row in db_counts:
                ret[ row["add_user_save_id"] ] = row["count"]
            return ret
        else:
            return {}
    ####################################

    def __getAddUserSaveIDCondition(self,add_user_saves):
        add_user_save_id_conds=map(lambda x:"add_user_save_id=%s"%x["add_user_save_id"],add_user_saves)
        return " or ".join(add_user_save_id_conds)
    
    def __createReportResult(self,add_user_saves,details,counts, date_type):
        details_dic=self.__convertDetailsToDic(details)
        self.__repairAddUserSaves(add_user_saves,details_dic,date_type,counts)
        return add_user_saves
    
    def __convertDetailsToDic(self,details):
        """
            convert details to a dic in format {add_user_save_id:(list of user_ids,list of usernames, list of passwords)}
        """
        dic = {}
        for add_user_save_id in details:
            dic[add_user_save_id]=[[],[],[]]
            for row in details[add_user_save_id]:
                dic[add_user_save_id][0].append(row["user_id"])
                dic[add_user_save_id][1].append(row["username"])
                dic[add_user_save_id][2].append(row["password"])

        return dic

    def __repairAddUserSaves(self,add_user_saves,details_dic,date_type,counts):
        for add_user_save in add_user_saves:
            add_user_save["add_date_formatted"]=AbsDate(add_user_save["add_date"],"gregorian").getDate(date_type)
            add_user_save["admin_name"]=admin_main.getLoader().getAdminByID(add_user_save["admin_id"]).getUsername()
            add_user_save["type_str"]=user_main.getAddUserSaveActions().getIDTypeStr(add_user_save["type"])
            try:
                add_user_save["details"]=details_dic[add_user_save["add_user_save_id"]]
            except KeyError:
                add_user_save["details"]=((),(),())
            
            if counts.has_key(add_user_save["add_user_save_id"]):
                add_user_save["users_count"]=counts[add_user_save["add_user_save_id"]]
            

class AddUserSaveSearcher:
    def __init__(self,conds,admin_obj):
        """
            conds(dic): dic of conditions
            admin_obj(Admin instance): requester admin object
        """
        self.search_helper=AddUserSaveSearchHelper(conds,admin_obj)
    
    def applyConditions(self):
        add_user_save_table=self.search_helper.getTable("add_user_saves")
        details_table=self.search_helper.getTable("add_user_save_details")
        
        self.__addAdminCondition(add_user_save_table)
        
        add_user_save_table.exactSearch(self.search_helper,"add_user_save_id","add_user_save_id",MultiStr)

        self.search_helper.setCondValue("date_from_op",">=")    
        add_user_save_table.dateSearch(self.search_helper,"date_from","date_from_unit","date_from_op","add_date")

        self.search_helper.setCondValue("date_to_op","<")
        add_user_save_table.dateSearch(self.search_helper,"date_to","date_to_unit","date_to_op","add_date")
        
        add_user_save_table.exactSearch(self.search_helper,"type","type",lambda type_str:user_main.getAddUserSaveActions().getTypeID(type_str))

        add_user_save_table.likeStrSearch(self.search_helper,"comment","comment_op","comment")

        details_table.exactSearch(self.search_helper,"user_id","user_id",MultiStr)      

        details_table.likeStrSearch(self.search_helper,"username","username_op","username",MultiStr)

        
    def __addAdminCondition(self,add_user_save_table):
        admin_restricted=not self.search_helper.getRequesterObj().isGod() and self.search_helper.getRequesterObj().getPerms()["SEE SAVED USERNAME PASSWORDS"].isRestricted()
        if admin_restricted:
            add_user_save_table.getRootGroup().addGroup("admin_id=%s"%self.search_helper.getRequesterObj().getAdminID())
        else:
            add_user_save_table.exactSearch(self.search_helper,"admin","admin_id",lambda admin_username:admin_main.getLoader().getAdminByName(admin_username).getAdminID())
    ################################################################################
    def getAddUserSaves(self,_from,to,order_by,desc,date_type):
        self.__getAddUserSavesCheckInput(_from,to,order_by,desc)
        self.applyConditions()
        (total_rows,result)=self.search_helper.getAddUserSaves(_from,to,order_by,desc,date_type)
        return {"total_rows":total_rows,"result":result}

    def __getAddUserSavesCheckInput(self,_from,to,order_by,desc):
        if self.search_helper.hasCondFor("users_from","users_to"):
            users_from = to_int(self.search_helper.getCondValue("users_from"),"users from")
            users_to = to_int(self.search_helper.getCondValue("users_to"),"users to")
            report_lib.checkFromTo(users_from,users_to)
            
        report_lib.checkFromTo(_from,to)
        self.__checkOrderBy(order_by)
        
    def __checkOrderBy(self,order_by):
        if order_by not in ["add_date","type","admin_id"]:
            raise GeneralException(errorText("GENERAL","INVALID_ORDER_BY")%order_by)
        