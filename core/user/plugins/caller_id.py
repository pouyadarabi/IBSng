from core.user import user_plugin,user_main,attribute
from core.user.attr_updater import AttrUpdater
from core.user.attr_searcher import AttrSearcher
from core.user.attr_holder import AttrHolder
from core.ibs_exceptions import *
from core.errors import errorText
from core.lib.general import *
from core.lib.multi_strs import MultiStr
from core.lib.password_lib import Password,getPasswords
from core.lib import iplib,maclib
from core.ras import ras_main,msgs
from core.db import ibs_db,db_main
import itertools,string

attr_handler_name="caller id"
def init():
    user_main.getAttributeManager().registerHandler(CallerIDUserAttrHandler(),["caller_id"],["caller_id"],["caller_id"])

def _checkCallerID(caller_id):
    if not len(caller_id):
        return False
    
    return True

def checkCallerID(caller_id):
    if not _checkCallerID(caller_id):
        raise GeneralException(errorText("USER_ACTIONS","BAD_CALLER_ID")%caller_id)

class CallerIDUserAttrUpdater(AttrUpdater):

    def changeInit(self,caller_id):
        """
            caller_id(string): an multi string of caller_ids
        """
        self.registerQuery("user","change",self.changeQuery,[])
        self.caller_ids = MultiStr(caller_id)
        
    def deleteInit(self):
        self.registerQuery("user","delete",self.deleteQuery,[])

#######################################
    def checkInput(self,src,action,dargs):
        map(dargs["admin_obj"].canChangeVoIPAttrs,dargs["users"].itervalues())
    
    def __checkCallerID(self,caller_ids,users):
        if len(caller_ids)<len(users):
            raise GeneralException(errorText("USER_ACTIONS","CALLER_ID_MAC_COUNT_NOT_MATCH")%(len(users),len(caller_ids)))

        cur_caller_ids = []
        for loaded_user in users.itervalues():
            if loaded_user.userHasAttr("caller_id"):
                cur_caller_ids += loaded_user.getUserAttrs()["caller_id"]
            
        to_check_caller_ids = []
        
        for caller_id in caller_ids:
            checkCallerID(caller_id)    
        
            if caller_id not in cur_caller_ids:
                to_check_caller_ids.append(caller_id)
            
        exists = self.callerIDExists(to_check_caller_ids)
        if len(exists):
            raise GeneralException(errorText("USER_ACTIONS","CALLER_ID_EXISTS")%",".join(exists))
        

    def __changeCheckInput(self,users):
        self.__checkCallerID(self.caller_ids, users)

########################################################
    def changeQuery(self,ibs_query,src,action,**args):
        admin_obj=args["admin_obj"]
        users=args["users"]
        
        self.__changeCheckInput(users)
        
        i = 0

        for user_id in users:
            loaded_user=users[user_id]

            if loaded_user.hasAttr("caller_id"):
                ibs_query += self.__deleteUserCallerIDsQuery(user_id)
                old_caller_id = ",".join(loaded_user.getUserAttrs()["caller_id"])

            else:
                old_caller_id = self.AUDIT_LOG_NOVALUE

            if i == len(users)-1: #last user?
                updated_caller_ids = self.caller_ids[i:]
            else:
                updated_caller_ids = (self.caller_ids[i],)

            ibs_query += self.__insertCallerIDsQuery(user_id, updated_caller_ids)

            if defs.USER_AUDIT_LOG:
                ibs_query += user_main.getUserAuditLogManager().userAuditLogQuery(args["admin_obj"].getAdminID(),
                                                                              True,
                                                                              loaded_user.getUserID(),
                                                                              "caller_id",
                                                                              old_caller_id,
                                                                              ",".join(updated_caller_ids))

            i+=1

        return ibs_query

################################################
    def deleteQuery(self,ibs_query,src,action,**args):
        users=args["users"]

        for user_id in users:
            loaded_user=users[user_id]
            if not loaded_user.userHasAttr("caller_id"):
                continue
                
            ibs_query += self.__deleteUserCallerIDsQuery(user_id)

            if defs.USER_AUDIT_LOG:
                ibs_query += user_main.getUserAuditLogManager().userAuditLogQuery(args["admin_obj"].getAdminID(),
                                                                              True,
                                                                              loaded_user.getUserID(),
                                                                              "caller_id",
                                                                              loaded_user.getUserAttrs()["caller_id"],
                                                                              self.AUDIT_LOG_NOVALUE)

        return ibs_query

###############################################
    def __deleteUserCallerIDsQuery(self, user_id):
        return ibs_db.createDeleteQuery("caller_id_users","user_id=%s"%user_id)

    def __insertCallerIDsQuery(self,user_id, caller_ids):
        return "".join(map(lambda caller_id: ibs_db.createInsertQuery("caller_id_users",
                                                                {"caller_id":dbText(caller_id),
                                                                "user_id":user_id}), caller_ids))

##########################################################
    def callerIDExists(self,caller_ids):
        """
            check if caller_ids currently exists in caller_id_users
            caller_ids(iterable object can be multistr or list): caller_ids that will be checked
            return a list of exists macs
            NOTE: This is not thread safe 
            XXX: test & check where_clause length
        """
        if len(caller_ids)==0:
            return []
        where_clause=" or ".join(map(lambda c:"caller_id=%s"%dbText(c),caller_ids))
        cids_db=db_main.getHandle().get("caller_id_users",where_clause,0,-1,"",["caller_id"])
        return [m["caller_id"] for m in cids_db]




class CallerIDAttrSearcher(AttrSearcher):
    def run(self):
        cid_table=self.getSearchHelper().getTable("caller_id_users")
        cid_table.likeStrSearch(self.getSearchHelper(),
                                   "caller_id",
                                   "caller_id_op",
                                   "caller_id",
                                   MultiStr)


class CallerIDAttrHolder(AttrHolder):
    def __init__(self,caller_ids):
        self.caller_ids = caller_ids

    def getParsedDic(self):
        return {"caller_id":",".join(self.caller_ids)}

class CallerIDUserAttrHandler(attribute.AttributeHandler):
    def __init__(self):
        attribute.AttributeHandler.__init__(self,attr_handler_name)
        self.registerAttrUpdaterClass(CallerIDUserAttrUpdater,["caller_id"])
        self.registerAttrSearcherClass(CallerIDAttrSearcher)
        self.registerAttrHolderClass(CallerIDAttrHolder,["caller_id"])
        