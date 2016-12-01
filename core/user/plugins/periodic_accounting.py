from core.user import user_plugin,user_main,attribute
from core.user.attr_updater import AttrUpdater
from core.user.attr_holder import AttrHolder
from core.user.attr_searcher import AttrSearcher
from core.ibs_exceptions import *
from core.lib.time_lib import *
from core.lib.date import *
from core import defs
import time,types

PACCOUNTING_DEBUG=False

def init():
    user_main.getUserPluginManager().register("time_periodic_accounting_monthly",MonthlyTimePeriodicAccounting)
    user_main.getUserPluginManager().register("traffic_periodic_accounting_monthly",MonthlyTrafficPeriodicAccounting)
    user_main.getUserPluginManager().register("time_periodic_accounting_daily",DailyTimePeriodicAccounting)
    user_main.getUserPluginManager().register("traffic_periodic_accounting_daily",DailyTrafficPeriodicAccounting)

    user_main.getAttributeManager().registerHandler(MonthlyTimeAttrHandler(),["time_periodic_accounting_monthly"],["time_periodic_accounting_monthly"])
    user_main.getAttributeManager().registerHandler(MonthlyTrafficAttrHandler(),["traffic_periodic_accounting_monthly"],["traffic_periodic_accounting_monthly"])
    user_main.getAttributeManager().registerHandler(DailyTimeAttrHandler(),["time_periodic_accounting_daily"],["time_periodic_accounting_daily"])
    user_main.getAttributeManager().registerHandler(DailyTrafficAttrHandler(),["traffic_periodic_accounting_daily"],["traffic_periodic_accounting_daily"])

    user_main.getAttributeManager().registerHandler(MonthlyTimeUsageAttrHandler(),["time_periodic_accounting_monthly_usage"],[],[],[periodicAccountingPostParser])
    user_main.getAttributeManager().registerHandler(MonthlyTrafficUsageAttrHandler(),["traffic_periodic_accounting_monthly_usage"])
    user_main.getAttributeManager().registerHandler(DailyTimeUsageAttrHandler(),["time_periodic_accounting_daily_usage"])
    user_main.getAttributeManager().registerHandler(DailyTrafficUsageAttrHandler(),["traffic_periodic_accounting_daily_usage"])


class BasePeriodicAccounting(user_plugin.AttrCheckUserPlugin):
    def __init__(self,user_obj, reset_type, key):
        """
            reset_type(str): monthly or daily
            key(str): key of attribute. the key itself should show the value of attribute
                      words _reset , _limit, _usage is appended to key name for other related attributes
        """
        user_plugin.AttrCheckUserPlugin.__init__(self,user_obj,key)
        self.key = key
        self.reset_type = reset_type
        self._initValues()

    def _initValues(self):
        if self.hasAttr():
            self.__initBasicValues()
            if self.user_obj.getUserAttrs().userHasAttr("%s_reset"%self.key):
                self.next_reset = long(self.user_obj.getUserAttrs()["%s_reset"%self.key]) #epoch
                self.__setInitialUsage()
                self.first_login = False #is this the first time we logged in with this value of paccounting
                self.commit_next_reset = False
                
                self._checkResetTimer()
            else:
                self._resetTimer()
                self.first_login = True

            self.usage = 0 #partial usages
            self.instance_start_value = []
    
    def __initBasicValues(self):
        self.value = self.user_obj.getUserAttrs()[self.key] #jalali/gregorian/number of days
        self.limit = long(self.user_obj.getUserAttrs()["%s_limit"%self.key]) #seconds
        

    def __setInitialUsage(self):
        self.initial_usage = long(self.user_obj.getUserAttrs()["%s_usage"%self.key])  #seconds
    ################################
    def _checkResetTimer(self):
        """
            check if it's time to reset
        """
        if self.next_reset <= time.time():
            self._resetTimer()
        
    def _resetTimer(self):      
        self.usage = 0
        self.initial_usage = 0
        self.__setNextReset()

    def __setNextReset(self):
        self.next_reset = self._calcNextReset(self.reset_type,self.value)    
        self.commit_next_reset = True
        
    def _calcNextReset(self, _type, value):
        if _type == "daily":
            if hasattr(self,"next_reset") and self.next_reset:
                base = self.next_reset
            else:
                base = time.time() - secondsFromMorning()

            increment = long(value) * 3600 * 24
            
            next_reset = base + increment
            while next_reset < time.time():
                next_reset += increment
                
            return next_reset
            
        elif _type == "monthly":
            if self.value == "gregorian":
                return getGregorianNextMonthEpoch()
            else:
                return getJalaliNextMonthEpoch()

    def _quotaFinished(self):
        """
            return true if quota of user has been finished
        """
        if self._calcUsage() >= self.limit:
            return True
        return False

    ###################################
    def s_commit(self):
        logout_instance = 0
        for instance in xrange(1,self.user_obj.instances+1):
            if self.user_obj.getInstanceInfo(instance).has_key("logout_ras_msg"):
                logout_instance = instance
                break
        
        if not logout_instance:
            toLog("PeriodicAccounting: commit can't find logout instance for user %s"%self.user_obj.getUserID(),LOG_ERROR)
            return
    
        instance_usage = self._calcUsageForInstance(logout_instance)
        self.usage += instance_usage
        query = self._commitUsageQuery(self.first_login)

        if self.commit_next_reset:
            query += self._commitNextResetQuery(self.first_login)
            self.commit_next_reset = False

        if self.first_login: #do not insert again
            self.first_login = False

        return query

    def _commitUsageQuery(self, first_login):
        usage = long(self.usage + self.initial_usage)
        if first_login:
            return user_main.getActionManager().insertUserAttrQuery(self.user_obj.getUserID(),
                                                                "%s_usage"%self.key,
                                                                usage)

        else:
            return user_main.getActionManager().updateUserAttrQuery(self.user_obj.getUserID(),
                                                                "%s_usage"%self.key,
                                                                usage)

    def _commitNextResetQuery(self, first_login):
        if first_login:
            return user_main.getActionManager().insertUserAttrQuery(self.user_obj.getUserID(),
                                                                "%s_reset"%self.key,
                                                                long(self.next_reset))
        else:
            return user_main.getActionManager().updateUserAttrQuery(self.user_obj.getUserID(),
                                                                "%s_reset"%self.key,
                                                                long(self.next_reset))
    ###################################
    def _calcUsage(self):
        """
            Children should override this
        """
        pass

    def _calcUsageForInstance(self, instance):
        """
            Children should override this
        """
        pass

    ###################################
    def _getStartValue(self, instance):
        """
            Children should override this
        """
        pass

    #####################################
    def _getQuotaFinishedErrorText(self, include_key):
        """
            Children should override this
        """
        pass

    #####################################
    def s_login(self, ras_msg):
        if ras_msg.hasAttr("start_accounting"):
            start_value = self._getStartValue(self.user_obj.instances)
        else:
            start_value = None
        
        self.instance_start_value.append(start_value)

        if self._quotaFinished():
            raise LoginException(self._getQuotaFinishedErrorText(True))
    
    def s_update(self, ras_msg):
        if ras_msg.hasAttr("start_accounting"):
            instance = self.user_obj.getInstanceFromRasMsg(ras_msg)
            self.instance_start_value[instance-1] = self._getStartValue(instance)
    
    ################################
    def _setStartValues(self):
        for instance in xrange(1,self.user_obj.instances+1):
            self.instance_start_value[instance-1] = self._getStartValue(instance)

    def s_canStayOnline(self):
        result=self.createCanStayOnlineResult()
        if self.next_reset <= time.time():
            self._resetTimer()
            self._setStartValues()
        
        if self._quotaFinished():
            result.setKillForAllInstances(self._getQuotaFinishedErrorText(False),self.user_obj.instances)
        else:
            if PACCOUNTING_DEBUG:
                toLog("Paccounting: user %s next reset is %s"%(self.user_obj.getUserID(), self.next_reset - time.time()), LOG_DEBUG)
                toLog("Paccounting: user %s end quota time is %s"%(self.user_obj.getUserID(), self._calcEndQuotaTime()), LOG_DEBUG)
            result.newRemainingTime(self.next_reset - time.time())
            result.newRemainingTime(self._calcEndQuotaTime())

        return result
        
    def _calcEndQuotaTime(self):
        """
            Children should override this
        """
        pass
    ################################
    def s_logout(self, instance, ras_msg):
        if len(self.instance_start_value) >= instance:
            
            del(self.instance_start_value[instance-1])
        
    ################################
    def _reload(self):
        """
            do not call AttrChecker reload. This plugin should be initialized on
            user login, otherwise the instances dictionary would be corrupted.
            XXX: This can be fixed by updating instances and usage always
        """
        if self.hasAttr():
            if self.user_obj.getUserAttrs().hasAttr(self.key):
                old_value = self.value
                self.__initBasicValues()
                if old_value != self.value:
                    self._resetTimer()
                    self._setStartValues()
                    self.first_login = True
                elif self.user_obj.getUserAttrs().userHasAttr("%s_usage"%self.key):
                    self.__setInitialUsage()
            else:
                self._setHasAttr(self.key)
        
            
################################
class TimePeriodicAccounting(BasePeriodicAccounting):

    def _calcEndQuotaTime(self):
        return self._calcTimelyEndQuotaTime()

    def _calcTimelyEndQuotaTime(self):
        return (self.limit - self._calcUsage()) / self.user_obj.instances

    ############################
    def _calcUsage(self):
        return self._calcTimelyUsage()

    def _calcUsageForInstance(self, instance):
        return self._calcTimelyUsageForInstance(instance)

    def _calcTimelyUsage(self):
        usage = 0
        for instance in xrange(1,self.user_obj.instances+1):
            usage += self._calcTimelyUsageForInstance(instance)
        return usage + self.usage + self.initial_usage

    def _calcTimelyUsageForInstance(self, instance):
        if self.instance_start_value[instance-1] != None:
            return time.time() - self.instance_start_value[instance-1]
        
        return 0
    ############################
    def _getQuotaFinishedErrorText(self, include_key):
        return self._getTimeQuotaFinishedErrorText(include_key)

    def _getTimeQuotaFinishedErrorText(self, include_key):
        return errorText("USER_LOGIN","TIMELY_QUOTA_EXCEEDED",include_key)

    ############################
    def _getStartValue(self, instance):
        return self._getTimelyStartValue(instance)

    def _getTimelyStartValue(self, instance):
        return time.time()

######################################
class TrafficPeriodicAccounting(BasePeriodicAccounting):
    def _calcEndQuotaTime(self):
        return self._calcTrafficEndQuotaTime()

    def _calcTrafficEndQuotaTime(self):
        if not self.user_obj.isNormalUser():
            return defs.MAXLONG
    
        instance_share = (self.limit - self._calcUsage()) / self.user_obj.instances
        remaining_time = 0
        for instance in xrange(1, self.user_obj.instances+1):
            try:
                remaining_time += instance_share / (self.user_obj.charge_info.effective_rules[instance-1].getAssumedKPS() * 1024.0)
            except:
                logException(LOG_DEBUG)

        return remaining_time
    ############################
    def _calcUsage(self):
        return self._calcTrafficUsage()

    def _calcUsageForInstance(self, instance):
        return self._calcTrafficUsageForInstance(instance)

    def _calcTrafficUsage(self):
        if not self.user_obj.isNormalUser():
            return 0
            
        usage = 0
        for instance in xrange(1,self.user_obj.instances+1):
            usage += self._calcTrafficUsageForInstance(instance)
        return usage + self.usage + self.initial_usage

    def _calcTrafficUsageForInstance(self, instance):
        if self.instance_start_value[instance-1] != None:
            return self._getTrafficUsage(instance) - self.instance_start_value[instance-1]
        return 0
    
    def _getTrafficUsage(self, instance):
        if not self.user_obj.isNormalUser():
            return 0
            
        in_bytes,out_bytes = self.user_obj.getTypeObj().getInOutBytes(instance)[:2]
        return in_bytes + out_bytes

    ############################
    def _getQuotaFinishedErrorText(self, include_key):
        return self._getTrafficQuotaFinishedErrorText(include_key)

    def _getTrafficQuotaFinishedErrorText(self, include_key):
        return errorText("USER_LOGIN","TRAFFIC_QUOTA_EXCEEDED",include_key)


    ############################
    def _getStartValue(self, instance):
        return self._getTrafficStartValue(instance)

    def _getTrafficStartValue(self, instance):
        return self._getTrafficUsage(instance)

class MonthlyTimePeriodicAccounting(TimePeriodicAccounting):
    def __init__(self,user_obj):
        TimePeriodicAccounting.__init__(self, user_obj, "monthly", "time_periodic_accounting_monthly")

class MonthlyTrafficPeriodicAccounting(TrafficPeriodicAccounting):
    def __init__(self,user_obj):
        TrafficPeriodicAccounting.__init__(self, user_obj, "monthly", "traffic_periodic_accounting_monthly")

class DailyTimePeriodicAccounting(TimePeriodicAccounting):
    def __init__(self,user_obj):
        TimePeriodicAccounting.__init__(self, user_obj, "daily", "time_periodic_accounting_daily")

class DailyTrafficPeriodicAccounting(TrafficPeriodicAccounting):
    def __init__(self,user_obj):
        TrafficPeriodicAccounting.__init__(self, user_obj, "daily", "traffic_periodic_accounting_daily")


#######################################################################################################
class PeriodicAccountingAttrUpdater(AttrUpdater):
    def __init__(self, key):
        self.key = key
        AttrUpdater.__init__(self,key)

    def checkInput(self,src,action,arg_dic):
        admin_obj = arg_dic["admin_obj"]
        admin_obj.canDo("CHANGE PERIODIC ACCOUNTING ATTRIBUTES")

        if action == "change":
            try:
                self.limit=long(self.limit)
            except ValueError:
                raise GeneralException(errorText("USER_ACTIONS","PERIODIC_ACCOUNING_LIMIT_INVALID"))


    def changeInit(self, value, limit):
        self.value = value
        self.limit = limit
        self.registerQuery("user","change",self.changeQuery,[])
        self.registerQuery("group","change",self.changeQuery,[])


    def changeQuery(self,ibs_query,src,action,**args):
        update_dic = {self.key:self.value,
                     "%s_limit"%self.key:self.limit}

        if src == "user":
            ibs_query = self._changeUserAttr(ibs_query, update_dic, args["users"], args["admin_obj"])
        
            for user_id in args["users"]:
                loaded_user = args["users"][user_id]
                if loaded_user.hasAttr(self.key) and loaded_user.getUserAttrs()[self.key] != str(self.value):
                    ibs_query = self._deleteUserAttr(ibs_query, ["%s_reset"%self.key, "%s_usage"%self.key], {user_id:loaded_user}, args["admin_obj"])

        elif src == "group":
            ibs_query = self._changeGroupAttr(ibs_query, update_dic, args["group_obj"], args["admin_obj"])
    
        return ibs_query        
        
        
    def deleteInit(self):
        self.useGenerateQuery([self.key, "%s_limit"%self.key, "%s_reset"%self.key, "%s_usage"%self.key])


    def auditLogPrepareValue(self,attr_name, value):
        if attr_name.startswith("traffic") and attr_name.endswith("_limit"):
            return "%sM"%(long(value)/(1024*1024))
        elif attr_name.startswith("time") and attr_name.endswith("_limit"):
            return formatDuration(long(value))
        elif attr_name.endswith("_reset") or attr_name.endswith("_usage") and value == None:
            return self.AUDIT_LOG_NOVALUE
        else:
            return value

    def genQueryAuditLogPrepareOldValue(self,attr_name, old_value):
        return self.auditLogPrepareValue(attr_name, old_value)

    def genQueryAuditLogPrepareNewValue(self,attr_name, new_value):
        return self.auditLogPrepareValue(attr_name, new_value)


class MonthlyPeriodicAccountingAttrUpdater(PeriodicAccountingAttrUpdater):
    def __init__(self, key):
        PeriodicAccountingAttrUpdater.__init__(self, key)

    def checkInput(self,src,action,arg_dic):
        PeriodicAccountingAttrUpdater.checkInput(self, src, action, arg_dic)
        if action == "change":
            if self.value not in ("jalali", "gregorian"):
                raise GeneralException(errorText("USER_ACTIONS","MONTHLY_PERIODIC_ACCOUNING_VALUE_INVALID"))

class DailyPeriodicAccountingAttrUpdater(PeriodicAccountingAttrUpdater):
    def __init__(self, key):
        PeriodicAccountingAttrUpdater.__init__(self, key)

    def checkInput(self,src,action,arg_dic):
        PeriodicAccountingAttrUpdater.checkInput(self, src, action, arg_dic)
        if action == "change":
            try:
                self.value=int(self.value)
            except ValueError:
                raise GeneralException(errorText("USER_ACTIONS","DAILY_PERIODIC_ACCOUNING_VALUE_INVALID"))

            if self.value <= 0:
                raise GeneralException(errorText("USER_ACTIONS","DAILY_PERIODIC_ACCOUNING_VALUE_INVALID"))


############################################################################################
class PeriodicAccountingUsageAttrUpdater(AttrUpdater):
    def __init__(self, usage_name):
        self.usage_name = usage_name
        AttrUpdater.__init__(self, usage_name)

    def checkInput(self,src,action,arg_dic):
        admin_obj = arg_dic["admin_obj"]
        admin_obj.canDo("CHANGE PERIODIC ACCOUNTING USAGE")

        if action == "change":
            try:
                self.usage = long(self.usage)
            except ValueError:
                raise GeneralException(errorText("USER_ACTIONS","PERIODIC_ACCOUNING_USAGE_INVALID"))


    def changeInit(self, usage):
        self.registerQuery("user","change",self.changeQuery,[])
        self.usage = usage

    def changeQuery(self,ibs_query,src,action,**args):
        users=args["users"]
        
        for user_id in users:
            loaded_user = users[user_id]

            if loaded_user.userHasAttr(self.usage_name):

                usage = long(loaded_user.getUserAttrs()[self.usage_name]) + self.usage
                ibs_query += user_main.getActionManager().updateUserAttrQuery(loaded_user.getUserID(),
                                                                              self.usage_name,
                                                                              usage)
            
                if defs.USER_AUDIT_LOG:
                    old_value = self.auditLogPrepareValue(self.usage_name, loaded_user.getUserAttrs()[self.usage_name])
                    new_value = self.auditLogPrepareValue(self.usage_name, usage)
                    ibs_query += user_main.getUserAuditLogManager().userAuditLogQuery(args["admin_obj"].getAdminID(),
                                                                              True,
                                                                              loaded_user.getUserID(),
                                                                              self.usage_name,
                                                                              old_value,
                                                                              new_value
                                                                              )

        return ibs_query

    def auditLogPrepareValue(self,attr_name, value):
        if attr_name.startswith("traffic") and attr_name.endswith("_usage"):
            return "%sM"%(long(value)/(1024*1024))
        elif attr_name.startswith("time") and attr_name.endswith("_usage"):
            return formatDuration(long(value))


###############################################################################
def periodicAccountingPostParser(_id, _type, raw_attrs, parsed_attrs, date_type):
    if _type != "user":
        return

    loaded_user = user_main.getUserPool().getUserByID(_id)
    if loaded_user.isOnline():
        user_obj = user_main.getOnline().getUserObj(_id)
        if not user_obj:
            return
        
        for key in ("time_periodic_accounting_monthly","traffic_periodic_accounting_monthly","time_periodic_accounting_daily","traffic_periodic_accounting_daily"):
            plugin_obj = getattr(user_obj,key)
            if plugin_obj.hasAttr():
                parsed_attrs["%s_usage"%key]=str(plugin_obj._calcUsage()) #maybe it's too big for a long value
                parsed_attrs["%s_reset"%key]=AbsDateFromEpoch(plugin_obj.next_reset).getDate(date_type)
    else:
        for key in ("time_periodic_accounting_monthly","traffic_periodic_accounting_monthly","time_periodic_accounting_daily","traffic_periodic_accounting_daily"):
            if loaded_user.userHasAttr("%s_reset"%key):
                parsed_attrs["%s_usage"%key]=loaded_user.getUserAttrs()["%s_usage"%key]
                parsed_attrs["%s_reset"%key]=AbsDateFromEpoch(long(loaded_user.getUserAttrs()["%s_reset"%key])).getDate(date_type)
            



###############################################################################
class MonthlyTimeAttrHandler(attribute.AttributeHandler):
    def __init__(self):
        attribute.AttributeHandler.__init__(self, "time_periodic_accounting_monthly")
        self.registerAttrUpdaterClass(MonthlyPeriodicAccountingAttrUpdater,["time_periodic_accounting_monthly","time_periodic_accounting_monthly_limit"])

class MonthlyTrafficAttrHandler(attribute.AttributeHandler):
    def __init__(self):
        attribute.AttributeHandler.__init__(self, "traffic_periodic_accounting_monthly")
        self.registerAttrUpdaterClass(MonthlyPeriodicAccountingAttrUpdater,["traffic_periodic_accounting_monthly","traffic_periodic_accounting_monthly_limit"])

class DailyTimeAttrHandler(attribute.AttributeHandler):
    def __init__(self):
        attribute.AttributeHandler.__init__(self, "time_periodic_accounting_daily")
        self.registerAttrUpdaterClass(DailyPeriodicAccountingAttrUpdater,["time_periodic_accounting_daily","time_periodic_accounting_daily_limit"])

class DailyTrafficAttrHandler(attribute.AttributeHandler):
    def __init__(self):
        attribute.AttributeHandler.__init__(self, "traffic_periodic_accounting_daily")
        self.registerAttrUpdaterClass(DailyPeriodicAccountingAttrUpdater,["traffic_periodic_accounting_daily","traffic_periodic_accounting_daily_limit"])

class MonthlyTimeUsageAttrHandler(attribute.AttributeHandler):
    def __init__(self):
        attribute.AttributeHandler.__init__(self, "time_periodic_accounting_monthly_usage")
        self.registerAttrUpdaterClass(PeriodicAccountingUsageAttrUpdater,["time_periodic_accounting_monthly_usage"])

class MonthlyTrafficUsageAttrHandler(attribute.AttributeHandler):
    def __init__(self):
        attribute.AttributeHandler.__init__(self, "traffic_periodic_accounting_monthly_usage")
        self.registerAttrUpdaterClass(PeriodicAccountingUsageAttrUpdater,["traffic_periodic_accounting_monthly_usage"])

class DailyTimeUsageAttrHandler(attribute.AttributeHandler):
    def __init__(self):
        attribute.AttributeHandler.__init__(self, "time_periodic_accounting_daily_usage")
        self.registerAttrUpdaterClass(PeriodicAccountingUsageAttrUpdater,["time_periodic_accounting_daily_usage"])

class DailyTrafficUsageAttrHandler(attribute.AttributeHandler):
    def __init__(self):
        attribute.AttributeHandler.__init__(self, "traffic_periodic_accounting_daily_usage")
        self.registerAttrUpdaterClass(PeriodicAccountingUsageAttrUpdater,["traffic_periodic_accounting_daily_usage"])

        
