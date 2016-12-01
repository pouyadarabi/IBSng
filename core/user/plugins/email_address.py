from core.user import user_plugin,user_main,attribute
from core.user.attr_updater import AttrUpdater
from core.user.attr_searcher import AttrSearcher
from core.ibs_exceptions import *
from core.errors import errorText
from core.lib.general import *
from core.lib.multi_strs import MultiStr
from core.db import db_main
from core.user import user_main

def init():
    user_main.getAttributeManager().registerHandler(EmailAddressAttrHandler(),["email_address"],["email_address"],[])

##########################################################
def emailAddressExists(email_address):
    """
        check if email_address currently exists
        email_address(iterable object can be multistr or list): username that will be checked
        return a list of exists email addresses
    """
    if len(email_address)==0:
        return []
    exists = []
    conds = map(lambda email:"attr_name='email_address' and attr_value=%s"%dbText(email),email_address)
    i = 0
    while i<len(conds):
        where_clause=" or ".join(conds[i:i+defs.POSTGRES_MAGIC_NUMBER])
        users_db=db_main.getHandle().get("user_attrs",where_clause,0,-1,"",["attr_value"])
        exists += [m["attr_value"] for m in users_db]
        i += defs.POSTGRES_MAGIC_NUMBER
    return exists
#########################################################

class EmailAddressAttrUpdater(AttrUpdater):
    def deleteCheckInput(self, src, action, dargs): #call on delete only
        dargs["admin_obj"].canDo("CHANGE MAILBOX")
        map(dargs["admin_obj"].canChangeNormalAttrs,dargs["users"].itervalues())

    def changeCheckInput(self,src,action,dargs):
        dargs["admin_obj"].canDo("CHANGE MAILBOX")
        
        users = dargs["users"]

        if src == "user":
            if len(users) != len(self.email_address):
                raise GeneralException(errorText("USER_ACTIONS","EMAIL_ADDRESS_COUNT_NOT_MATCH")%len(users),len(self.email_address))
            
            cur_emails=[]
            for loaded_user in users.itervalues():

                if loaded_user.hasAttr("email_address"):
                    cur_emails.append(loaded_user.getUserAttrs()["email_address"])

            to_check_emails=[]
            i = 0
            for loaded_user in dargs["users"].itervalues():
                dargs["admin_obj"].canChangeNormalAttrs(loaded_user)
                    
                (local_part, domain) = checkEmailAddress(self.email_address[i])
        
                if dargs["admin_obj"].hasPerm("LIMIT MAIL DOMAIN"):
                    dargs["admin_obj"].checkPerm("LIMIT MAIL DOMAIN", domain)
                
                if self.email_address.count(self.email_address[i])>1:
                    raise GeneralException(errorText("USER_ACTIONS","DUPLICATE_EMAIL_ADDRESS") % (self.email_address[i]))
                
                if self.email_address[i] not in cur_emails:
                    to_check_emails.append(self.email_address[i])
                
                i += 1

            exists=emailAddressExists(to_check_emails)
            if exists:
                raise GeneralException(errorText("USER_ACTIONS","EMAIL_ADDRESS_EXISTS")%",".join(exists))


    def changeInit(self,email_address):
        self.email_address=map(None,MultiStr(email_address))
        self.registerQuery("user","change",self.changeQuery,[])

    def deleteInit(self):
        self.registerQuery("user","delete",self.deleteQuery,[])

    def changeQuery(self,ibs_query,src,action,**args):

        self.changeCheckInput(src, action, args)

        self.users=args["users"]
        self.user_ids = self.users.keys()
        self.user_ids.sort()

        self.old_values=[]

        admin_obj=args["admin_obj"]

        i=0
        for user_id in self.user_ids:
            loaded_user=self.users[user_id]
        
            if loaded_user.userHasAttr("email_address"):
                ibs_query += self.updateEmailAddressAttrQuery(user_id,
                                                              self.email_address[i])
                old_value = loaded_user.getUserAttrs()["email_address"]

            else:
                ibs_query +=self.insertEmailAddressAttrQuery(user_id,
                                                              self.email_address[i])
                old_value = self.AUDIT_LOG_NOVALUE

            self.old_values.append(old_value)

            if defs.USER_AUDIT_LOG:
                ibs_query += user_main.getUserAuditLogManager().userAuditLogQuery(admin_obj.getAdminID(),
                                                                              True,
                                                                              loaded_user.getUserID(),
                                                                              "email_address",
                                                                              old_value,
                                                                              self.email_address[i])




            i+=1

        return ibs_query        
        



    def deleteQuery(self,ibs_query,src,action,**args):
        self.users=args["users"]
        self.user_ids=self.users.keys()
        self.old_values=[]

        for user_id in self.user_ids:
            loaded_user = self.users[user_id]
            old_value = self.AUDIT_LOG_NOVALUE
            
            if loaded_user.userHasAttr("email_address"):
                ibs_query += self.deleteEmailAddressAttrQuery(user_id)
                
                old_value = loaded_user.getUserAttrs()["email_address"]
                
                if defs.USER_AUDIT_LOG:
                    ibs_query += user_main.getUserAuditLogManager().userAuditLogQuery(args["admin_obj"].getAdminID(),
                                                                              True,
                                                                              loaded_user.getUserID(),
                                                                              "email_address",
                                                                              old_value,
                                                                              self.AUDIT_LOG_NOVALUE)

            self.old_values.append(old_value)
            
        return ibs_query


    def updateEmailAddressAttrQuery(self, user_id, email_address):
        return user_main.getActionManager().updateUserAttrQuery(user_id, "email_address", email_address)

    def insertEmailAddressAttrQuery(self, user_id, email_address):
        return user_main.getActionManager().insertUserAttrQuery(user_id, "email_address", email_address)

    def deleteEmailAddressAttrQuery(self, user_id):
        return user_main.getActionManager().deleteUserAttrQuery(user_id, "email_address")


    def postUpdate(self,src,action):
        toLog("%s %s %s %s"%(self.old_values,src,action,self.user_ids),LOG_DEBUG)
        i = 0
        for user_id in self.user_ids:
            loaded_user=self.users[user_id]
            
            if action=="change":
                if self.old_values[i] != self.email_address[i]: #email address changed
                    user_main.getMailActions().createMailbox(self.email_address[i])
                    if self.old_values[i] != self.AUDIT_LOG_NOVALUE:
                        user_main.getMailActions().deleteMailbox(self.old_values[i])
                    
            elif action=="delete":
                if self.old_values[i] != self.AUDIT_LOG_NOVALUE:
                    user_main.getMailActions().deleteMailbox(self.old_values[i])

            i += 1

class EmailAddressAttrSearcher(AttrSearcher):
    def run(self):
        search_helper=self.getSearchHelper()
        user_attrs=search_helper.getTable("user_attrs")
        user_attrs.likeStrSearch(search_helper,"email_address","email_address_op","email_address", MultiStr)


class EmailAddressAttrHandler(attribute.AttributeHandler):
    def __init__(self):
        attribute.AttributeHandler.__init__(self,"email_address")
        self.registerAttrUpdaterClass(EmailAddressAttrUpdater,["email_address"])
        self.registerAttrSearcherClass(EmailAddressAttrSearcher)
