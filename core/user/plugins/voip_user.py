from core.user import user_plugin,user_main,attribute
from core.user.attr_updater import AttrUpdater
from core.user.attr_searcher import AttrSearcher
from core.ibs_exceptions import *
from core.errors import errorText
from core.lib.general import *
from core.lib.multi_strs import MultiStr
from core.lib.password_lib import Password,getPasswords
from core.db.ibs_query import IBSQuery
from core.db import ibs_db,db_main
from core.server import handler,handlers_manager
from core import defs
import itertools

attr_handler_name="voip user"
def init():
    user_main.getAttributeManager().registerHandler(VoIPUserAttrHandler(),["voip_username","voip_password","voip_generate_password","voip_generate_password_len","voip_save_usernames"],["voip_username"],[])
    handlers_manager.getManager().registerHandler(VoIPUserHandler())
    user_main.getUserPluginManager().register("voip_user_plugin",VoIPUser)

    global actions
    actions=VoIPUserActions()

def getActionsManager():
    return actions

class VoIPUser(user_plugin.UserPlugin): 
    def login(self, ras_msg):
        if self.user_obj.isVoIPUser() and not self.user_obj.getUserAttrs().userHasAttr("voip_username"):
            return GeneralException(errorText("USER_LOGIN","NO_VOIP_USERNAME_DEFINED"))


    def update(self, ras_msg):
        if "called_ip" in ras_msg["update_attrs"]:
            instance=self.user_obj.getInstanceFromRasMsg(ras_msg)
            self.user_obj.getInstanceInfo(instance)["attrs"]["called_ip"]=ras_msg["called_ip"]


    def logout(self, instance, ras_msg):
        if self.user_obj.isVoIPUser() and ras_msg.hasAttr("disconnect_cause"):
            self.user_obj.getInstanceInfo(instance)["attrs"]["disconnect_cause"]=ras_msg["disconnect_cause"]

	#TODO: Fix in B Branch
        if self.user_obj.isVoIPUser() and ras_msg.hasAttr("called_ip"):
            self.user_obj.getInstanceInfo(instance)["attrs"]["called_ip"]=ras_msg["called_ip"]
        

###########################################
check_username_pattern=re.compile("[^A-Za-z0-9_\-\.]")
def _checkVoIPUsernameChars(username):
    if not len(username):
        return False
    if check_username_pattern.search(username) != None:
        return False
    return True
            
def checkVoIPUsernameChars(username):
    if not _checkVoIPUsernameChars(username):
        raise GeneralException(errorText("USER_ACTIONS","BAD_VOIP_USERNAME")%username)


##########################################################
def voipUsernameExists(voip_username):
    """
        check if voip_username currently exists
        voip_username(iterable object can be multistr or list): username that will be checked
        return a list of exists usernames
        NOTE: This is not thread safe 
        XXX: test & check where_clause length
    """
    if len(voip_username)==0:
        return []

    exists = []
    conds = map(lambda username:"voip_username=%s"%dbText(username),voip_username)
    i = 0
    while i<len(conds):
        where_clause=" or ".join(conds[i:i+defs.POSTGRES_MAGIC_NUMBER])
        users_db=db_main.getHandle().get("voip_users",where_clause,0,-1,"",["voip_username"])
        exists += [m["voip_username"] for m in users_db]
        i += defs.POSTGRES_MAGIC_NUMBER
    return exists
#########################################################

class VoIPUserAttrUpdater(AttrUpdater):

    def changeInit(self,voip_username,voip_password,generate_password,password_len,voip_save):
        """
            generate_passwd is an integer, 0 means don't generate password and use voip_passwords instead
            positive values are same as password_lib.getPasswords _type, see function comments
            
            voip_save(str): tells if we should save this username passwords in database so
                                username/passwords can be seen later, 
                                If set to False or empty string it means don't save
                                else it'll be passed as comment
                                
        """
        self.registerQuery("user","change",self.changeQuery,[])
        self.voip_username=voip_username
        self.voip_password=voip_password
        self.generate_password=generate_password
        self.password_len=to_int(password_len,"Password Length")
        self.voip_save=voip_save

    def deleteInit(self):
        self.registerQuery("user","delete",self.deleteQuery,[])

    #################################################
    def __parseVoIPAttrs(self):
        self.usernames=map(None,MultiStr(self.voip_username))
        if self.generate_password==0:
            pass_multi=MultiStr(self.voip_password)
            self.passwords=map(lambda x:Password(pass_multi[x]),range(len(self.usernames)))
        else:
            self.passwords=getPasswords(len(self.usernames),self.generate_password,self.password_len)
        
    ##################################################
    def checkInput(self,src,action,dargs):
        map(dargs["admin_obj"].canChangeVoIPAttrs,dargs["users"].itervalues())

    def __changeCheckInput(self,users,admin_obj):
        self.__checkUsernames(users)
        self.__checkPasswords()

    def __checkPasswords(self):
        map(lambda password:password.checkPasswordChars(),self.passwords)
        if self.password_len<0 or self.password_len>30:
            raise GeneralException(errorText("USER_ACTIONS","INVALID_PASSWORD_LENGTH")%self.password_len)


    def __checkUsernames(self,users):
        if len(self.usernames) != len(users):
            raise GeneralException(errorText("USER_ACTIONS","VOIP_USER_COUNT_NOT_MATCH")%(len(users),len(self.usernames)))
        
        cur_voip_usernames = []
        for loaded_user in users.itervalues():
            if loaded_user.userHasAttr("voip_username"):
                cur_voip_usernames.append(loaded_user.getUserAttrs()["voip_username"])
        
        to_check_usernames = [] #check users for exitence
        for username in self.usernames:
            checkVoIPUsernameChars(username)

            if self.usernames.count(username) > 1:
                raise GeneralException(errorText("USER_ACTIONS","DUPLICATE_USERNAME") % (username))

            if username not in cur_voip_usernames:
                to_check_usernames.append(username)    
        
        exists=voipUsernameExists(to_check_usernames)
        if exists:
            raise GeneralException(errorText("USER_ACTIONS","VOIP_USERNAME_EXISTS")%",".join(exists))

    #####################################################
    def changeQuery(self,ibs_query,src,action,**args):
        admin_obj=args["admin_obj"]
        users=args["users"]
        user_ids = users.keys()
        user_ids.sort()

        
        self.__parseVoIPAttrs()
        self.__changeCheckInput(users,admin_obj)

        null_queries = IBSQuery()
        real_queries = IBSQuery()

        i = 0
        for user_id in user_ids:
            loaded_user = users[user_id]
            if loaded_user.userHasAttr("voip_username"):
                null_queries += self.updateVoIPUserAttrsToNullQuery(user_id)
                real_queries += self.updateVoIPUserAttrsQuery(user_id,
                                                           self.usernames[i],
                                                           self.passwords[i].getPassword())
                old_value = loaded_user.getUserAttrs()["voip_username"]
            else:
                real_queries += self.insertVoIPUserAttrsQuery(user_id,
                                                           self.usernames[i],
                                                           self.passwords[i].getPassword())
                
                old_value = self.AUDIT_LOG_NOVALUE

            if defs.USER_AUDIT_LOG:
                ibs_query += user_main.getUserAuditLogManager().userAuditLogQuery(args["admin_obj"].getAdminID(),
                                                                              True,
                                                                              loaded_user.getUserID(),
                                                                              "voip_username",
                                                                              old_value,
                                                                              self.usernames[i])

                
            i += 1

        ibs_query += null_queries
        ibs_query += real_queries

        if self.voip_save:
            user_main.getAddUserSaveActions().newAddUser(ibs_query,
                                                         user_ids,
                                                         self.usernames,
                                                         self.passwords,
                                                         admin_obj.getAdminID(),
                                                         "VoIP",
                                                         "")
        return ibs_query

    def deleteQuery(self,ibs_query,src,action,**args):
        users=args["users"]

        for user_id in users:
            loaded_user = users[user_id]
            if loaded_user.userHasAttr("voip_username"):
                ibs_query += self.deleteVoIPUserAttrsQuery(user_id)

                if defs.USER_AUDIT_LOG:
                    ibs_query += user_main.getUserAuditLogManager().userAuditLogQuery(args["admin_obj"].getAdminID(),
                                                                              True,
                                                                              loaded_user.getUserID(),
                                                                              "voip_username",
                                                                              loaded_user.getUserAttrs()["voip_username"],
                                                                              self.AUDIT_LOG_NOVALUE)
                
        return ibs_query
    ################################################
    def insertVoIPUserAttrsQuery(self,user_id,voip_username,voip_password):
        """
            insert user voip attributes in "voip_users" table
        """
        return ibs_db.createInsertQuery("voip_users",{"voip_username":dbText(voip_username),
                                                        "voip_password":dbText(voip_password),
                                                        "user_id":user_id})

    def updateVoIPUserAttrsToNullQuery(self,user_id):
        """
            update voip_username to null, we run into unique constraint violation, when updating multiple
            users. So we update them to null and then update to new username
        """
        return ibs_db.createUpdateQuery("voip_users",{"voip_username":"NULL"}
                                                       ,"user_id=%s"%user_id)


    def updateVoIPUserAttrsQuery(self,user_id,voip_username,voip_password):
        """
            update user voip attributes in "voip_users" table
        """
        return ibs_db.createUpdateQuery("voip_users",{"voip_username":dbText(voip_username),
                                                        "voip_password":dbText(voip_password),
                                                     },"user_id=%s"%user_id)

    def deleteVoIPUserAttrsQuery(self,user_id):
        """
            delete user voip attributes from "voip_users" table
        """
        return ibs_db.createDeleteQuery("voip_users","user_id=%s"%user_id)
        

class VoIPUserAttrSearcher(AttrSearcher):
    def run(self):
        voip_table=self.getSearchHelper().getTable("voip_users")
        voip_table.likeStrSearch(self.getSearchHelper(),
                                   "voip_username",
                                   "voip_username_op",
                                   "voip_username",
                                   MultiStr)

class NoVoIPUserAttrSearcher(AttrSearcher):
    def run(self):
        users_table=self.getSearchHelper().getTable("users")
        users_table.notInTable(self.getSearchHelper(),
                               "no_voip_username",
                               "voip_users",
                               "user_id")


class VoIPUserAttrHandler(attribute.AttributeHandler):
    def __init__(self):
        attribute.AttributeHandler.__init__(self,attr_handler_name)
        self.registerAttrUpdaterClass(VoIPUserAttrUpdater,
                                      ["voip_username",
                                      "voip_password",
                                      "voip_generate_password",
                                      "voip_generate_password_len",
                                      "voip_save_usernames"])
        self.registerAttrSearcherClass(VoIPUserAttrSearcher)
        self.registerAttrSearcherClass(NoVoIPUserAttrSearcher)

#############################################################
class VoIPUserHandler(handler.Handler):

    def __init__(self):
        handler.Handler.__init__(self,"voip_user")
        self.registerHandlerMethod("checkVoIPUsernameForAdd")
        self.registerHandlerMethod("changePassword")

    ############################################################
    def checkVoIPUsernameForAdd(self,request):
        """
            check if voip_username multi str arg is exists, and doesn't contain invalid characters
            current_username shows current usernames, so we don't run into situation that we print an error
            for username that belongs to this username
        """
        request.needAuthType(request.ADMIN)
        request.checkArgs("voip_username","current_username")
        request.getAuthNameObj().canChangeVoIPAttrs(None)
        usernames=self.__filterCurrentUsernames(request)
        bad_usernames=filter(lambda username: not _checkVoIPUsernameChars(username),usernames)
        exist_usernames=voipUsernameExists(usernames)
        return self.__createCheckAddReturnDic(bad_usernames,exist_usernames)

    def __filterCurrentUsernames(self,request):
        username=MultiStr(request["voip_username"])
        current_username=MultiStr(request["current_username"])
        return filter(lambda username: username not in current_username,username)

    def __createCheckAddReturnDic(self,bad_usernames,exist_usernames):
        ret={}
        if len(bad_usernames)!=0:
            ret[errorText("USER_ACTIONS","BAD_VOIP_USERNAME",False)%""]=bad_usernames
        if len(exist_usernames)!=0:
            ret[errorText("USER_ACTIONS","VOIP_USERNAME_EXISTS",False)%""]=exist_usernames
        return ret

    ###########################################################
    def changePassword(self,request):
        request.needAuthType(request.ADMIN,request.VOIP_USER)
            
        if request.hasAuthType(request.ADMIN):
            loaded_user = user_main.getUserPool().getUserByVoIPUsername(request["voip_username"])
            request.getAuthNameObj().canChangeVoIPAttrs(loaded_user)
            user_id = loaded_user.getUserID()
        else:   
            user_id = request.getAuthNameObj().getUserID()
            self.__checkOldPassword(request.getAuthNameObj(),request["old_password"])

        getActionsManager().changePassword(user_id, request["password"])

    def __checkOldPassword(self,loaded_user,old_password):
        if not Password(old_password) == loaded_user.getUserAttrs()["voip_password"]:
            raise GeneralException(errorText("USER_ACTIONS","WRONG_OLD_PASSWORD"))
        
class VoIPUserActions:
    def changePasswordByUsername(self, username, password):
        """
            change user password by his username
        """
        loaded_user=user_main.getUserPool().getUserByVoIPUsername(username)
        return self.changePassword(loaded_user.getUserID(), password)

    def changePassword(self, user_id, password):
        """
            user_id(int): should be valid user id
            password(str): new voip password of user
        """
        password = Password(password)
        self.__changePasswordCheckInput(password)
        self.__updatePasswordDB(user_id,password.getPassword())
        user_main.getActionManager().broadcastChange([user_id])

    def __changePasswordCheckInput(self,password):
        password.checkPasswordChars()

    def __updatePasswordDB(self,user_id,password):
        db_main.getHandle().transactionQuery(
                ibs_db.createUpdateQuery("voip_users",
                                         {"voip_password":dbText(password)},
                                         "user_id=%s"%user_id))

    def checkPassword(self, username, password):
        loaded_user=user_main.getUserPool().getUserByVoIPUsername(username)
        return Password(loaded_user.getUserAttrs()["voip_password"])==password

        
        