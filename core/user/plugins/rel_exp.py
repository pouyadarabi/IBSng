from core.user import user_plugin,user_main,attribute
from core.user.attr_updater import AttrUpdater
from core.user.attr_holder import AttrHolder
from core.user.attr_searcher import AttrSearcher
from core.ibs_exceptions import *
from core.lib.date import *
from core.errors import errorText
import time

attr_handler_name="rel exp date"

def init():
    user_main.getUserPluginManager().register("rel_exp_date",RelExpDate)
    user_main.getAttributeManager().registerHandler(RelExpDateAttrHandler(),["rel_exp_date"],["rel_exp_date"],["rel_exp_date"])
    user_main.getAttributeManager().registerHandler(FirstLoginAttrHandler(),[],["first_login"],["first_login"])


class RelExpDate(user_plugin.UserPlugin):
    def __init__(self,user_obj):
        user_plugin.UserPlugin.__init__(self,user_obj)
        #delay initialization of first login and value to login time
        
    def hasAttr(self):
        return self.user_obj.getUserAttrs().hasAttr("rel_exp_date")

    def __initFirstLogin(self, no_commit=False):
        self.__commit_first_login=False

        if self.__isFirstLogin():
            self.__first_login=long(self.__login_time)
            if not no_commit:
                self.__commit_first_login=True
                self.user_obj.getUserAttrs().setAttr("first_login",self.__first_login)

        else:
            self.__first_login=long(self.user_obj.getUserAttrs()["first_login"])

    def __initValues(self):
        if self.hasAttr():
            self.__rel_exp_date_time=self.__calcRelExpDateTime(self.__first_login,long(self.user_obj.getUserAttrs()["rel_exp_date"]))

    def __isFirstLogin(self):
        return not self.user_obj.getUserAttrs().hasAttr("first_login")
            
    def __calcRelExpDateTime(self,first_login,rel_exp_date_val):
        return first_login+rel_exp_date_val

    def __isRelExpired(self):
        """
            check if user has relative expiration date has reached
        """
        return self.__rel_exp_date_time<=time.time()

    def login(self,ras_msg):
        #TODO: Fix in B Branch to use loginTime
        
        #keep it here to set first_login if necessary
        self.__login_time = ras_msg.getTime()

        self.__initFirstLogin(ras_msg.hasAttr("no_commit"))
        self.__initValues()
        if self.hasAttr() and self.__isRelExpired():
            raise LoginException(errorText("USER_LOGIN","REL_EXP_DATE_REACHED"))

    def canStayOnline(self):
        if self.hasAttr():      
            result=self.createCanStayOnlineResult()
            if self.__isRelExpired():
                result.setKillForAllInstances(errorText("USER_LOGIN","REL_EXP_DATE_REACHED",False),self.user_obj.instances)
            else:
                result.newRemainingTime(self.__rel_exp_date_time-time.time())
            return result

    def commit(self):
        query=""
        if self.__commit_first_login:
            query+=user_main.getActionManager().insertUserAttrQuery(self.user_obj.getUserID(),
                                                                    "first_login",
                                                                    self.__first_login
                                                                    )
            self.__commit_first_login=False
        return query
        
    def _reload(self):
        #First option can be reset
        self.__initFirstLogin()
        self.__initValues()

            
    
class RelExpAttrUpdater(AttrUpdater):
        
    def changeInit(self,rel_exp_date,rel_exp_date_unit):
        self.rel_exp_date=rel_exp_date
        self.rel_exp_date_unit=rel_exp_date_unit
        self.rel_date_obj=RelativeDate(rel_exp_date,rel_exp_date_unit)

        try:
            self.rel_date_obj.check()
        except GeneralException:
            raise GeneralException(errorText("USER_ACTIONS","INVALID_REL_EXP_DATE"))

        self.useGenerateQuery(self.__createUpdateAttrsDic())
                
    def __createUpdateAttrsDic(self):
        return {"rel_exp_date":self.rel_date_obj.getDBDate()}

    def genQueryAuditLogPrepareOldValue(self,attr_name, old_value):
        return " ".join( map(str,RelativeDate(long(old_value),"Seconds").getFormattedDate()) )

    def genQueryAuditLogPrepareNewValue(self,attr_name, new_value):
        return " ".join( map(str,self.rel_date_obj.getFormattedDate()) )


    def userChangeQuery(self,ibs_query,src,action,**args):
        """
            unused
        """
        new_args=args.copy()
        for user_id in args["users"]:
            loaded_user=args["users"][user_id]
            new_args["attr_updater_attrs"]=self.__createUpdateAttrsDic()
            new_args["users"]={user_id:loaded_user}
            if loaded_user.hasAttr("first_login"):
                new_args["attr_updater_attrs"]["rel_exp_date_time"]=loaded_user.getUserAttrs()["first_login"]+self.rel_date_obj.getDateHours()*3600
            self.generateQuery(ibs_query,src,action,**new_args)


    def deleteInit(self):
        self.useGenerateQuery(["rel_exp_date"])


class FirstLoginAttrUpdater(AttrUpdater):
    def deleteInit(self):
        self.useGenerateQuery(["first_login"])

    def genQueryAuditLogPrepareOldValue(self,attr_name, old_value):
        return AbsDateFromEpoch(long(old_value)).getDate()
    

class RelExpValueAttrSearcher(AttrSearcher):
    def run(self):
        search_helper=self.getSearchHelper()
        if search_helper.hasCondFor("rel_exp_value","rel_exp_value_unit","rel_exp_value_op"):
            checkltgtOperator(search_helper.getCondValue("rel_exp_value_op"))
            rel_date_obj=RelativeDate(search_helper.getCondValue("rel_exp_value"),
                                      search_helper.getCondValue("rel_exp_value_unit"))
            for table in self.getUserAndGroupAttrsTable():
                table.search("rel_exp_date",(rel_date_obj.getDBDate(),),search_helper.getCondValue("rel_exp_value_op"),"integer")

class RelExpDateAttrSearcher(AttrSearcher):
    def run(self):
        search_helper=self.getSearchHelper()
        if search_helper.hasCondFor("rel_exp_date","rel_exp_date_unit","rel_exp_date_op"):
            checkltgtOperator(search_helper.getCondValue("rel_exp_date_op"))
            date_obj=AbsDateWithUnit(search_helper.getCondValue("rel_exp_date"),
                                      search_helper.getCondValue("rel_exp_date_unit"),False)

            
            search_helper.getTable("users").addGroup("user_id in (select rel_exp_date.user_id from  \
                    (select attr_value::bigint,user_id from user_attrs where attr_name='first_login') as first_login, \
                    (select attr_value::bigint,user_id from user_attrs where attr_name='rel_exp_date' \
                    union \
                    select group_attrs.attr_value::bigint,user_id from users,group_attrs \
                    where \
                    users.group_id=group_attrs.group_id and group_attrs.attr_name='rel_exp_date' and user_id not in \
                    (select user_attrs.user_id from user_attrs where user_attrs.attr_name='rel_exp_date')) \
                    as rel_exp_date \
                    where \
                    rel_exp_date.user_id=first_login.user_id and first_login.attr_value+rel_exp_date.attr_value %s %s )"%(search_helper.getCondValue("rel_exp_date_op"),date_obj.getEpochDate()))
    
class RelExpAttrHolder(AttrHolder):
    def __init__(self,rel_exp):
        self.rel_exp=rel_exp
        self.rel_date_obj=RelativeDate(rel_exp,"Seconds")

    def getParsedDic(self):
        (rel_exp_date,unit)=self.rel_date_obj.getFormattedDate()
        return {"rel_exp_date":rel_exp_date,"rel_exp_date_unit":unit}


class FirstLoginAttrHolder(AttrHolder):
    def __init__(self,first_login):
        self.first_login=AbsDateFromEpoch(long(first_login))

    def getParsedDic(self):
        return ({"first_login":self.first_login.getDate(self.date_type)})


class FirstLoginAttrSearcher(AttrSearcher):
    def run(self):
        search_helper=self.getSearchHelper()
        if search_helper.hasCondFor("first_login","first_login_unit","first_login_op"):
            checkltgtOperator(search_helper.getCondValue("first_login_op"))
            date_obj=AbsDateWithUnit(search_helper.getCondValue("first_login"),
                                      search_helper.getCondValue("first_login_unit"), False)
            self.getSearchHelper().getTable("user_attrs").search("first_login",
                                                                 (date_obj.getDate("epoch"),),
                                                                 search_helper.getCondValue("first_login_op"),
                                                                 "bigint")


class RelExpDateAttrHandler(attribute.AttributeHandler):
    def __init__(self):
        attribute.AttributeHandler.__init__(self,attr_handler_name)
        self.registerAttrUpdaterClass(RelExpAttrUpdater,["rel_exp_date","rel_exp_date_unit"])
        self.registerAttrHolderClass(RelExpAttrHolder,["rel_exp_date"])
        self.registerAttrSearcherClass(RelExpValueAttrSearcher)
        self.registerAttrSearcherClass(RelExpDateAttrSearcher)


class FirstLoginAttrHandler(attribute.AttributeHandler):
    def __init__(self):
        attribute.AttributeHandler.__init__(self,"first_login")
        self.registerAttrUpdaterClass(FirstLoginAttrUpdater,[])
        self.registerAttrHolderClass(FirstLoginAttrHolder,["first_login"])
        self.registerAttrSearcherClass(FirstLoginAttrSearcher)
