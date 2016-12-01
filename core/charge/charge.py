import threading
from core.lib.general import *
from core.lib.time_lib import *
from core import defs
from core.errors import errorText
from core.db import db_main
from core.charge.user_charge import *
from core.admin import admin_main
from core.ibs_exceptions import *
from core.errors import errorText



#-----------------------------------------------------------------------------------------------------------
class Charge:
    def __init__(self,charge_id,name,comment,admin_id,visible_to_all,_type):
        """
            charge_id (integer): unique charge id, db will assign a new id to each charge
            name (string): name of charge
            comment (string): comment
            admin_id (integer): id of admin who created this charge
            visible_default (boolean): if visible default is set to 1 then all admins can use this group without a 
                                       special permission
            _type (string): _type of charge (VoIP or Internet) 
        """

        self.charge_id=charge_id
        self.name=name
        self.comment=comment
        self.admin_id=admin_id
        self.visible_to_all=visible_to_all
        self._type=_type

    def getType(self):
        """
            return string representation of group
        """
        return self._type

    def isInternetCharge(self):
        return self.getType()=="Internet"

    def isVoIPCharge(self):
        return self.getType()=="VoIP"
        
    def getChargeID(self):
        return self.charge_id

    def getChargeName(self):
        return self.name

    def isVisibleToAll(self):
        return self.visible_to_all=="t"

    def getChargeInfo(self):
        return {"charge_id":self.getChargeID(),
                "charge_name":self.getChargeName(),
                "comment":self.comment,
                "creator":admin_main.getLoader()[self.admin_id].getUsername(),
                "charge_type":self._type,
                "visible_to_all":self.visible_to_all
                }

    def __str__(self):
        return "charge with name: %s"%(self.name)

    def initUser(self,user_obj):
        """
            called when a user logins
            
            user_obj: object of user
                    user_obj.instance show the instance of that logged in
            
        """
        pass

        
    def startAccounting(self,user_obj,instance):
        """
            call to notify accounting of user should be started
        """
        user_obj.charge_info.accounting_started[instance-1]=time.time()
        

    def logout(self,user_obj,instance): 
        """
            called when logout event of user occures or when the user login was not successful
        """
        pass


    def checkLimits(self,user_obj):
        """     
            called when an event (login,logout,rule change,credit finish..) occures, 
                
            returns (time_till_next_event,{dictionary of instance:kill reason}) 
            time_till_next_event == 0 means no event should be set
        """
        return (0,"Limited group")
        
    def calcUserAvailableTime(self,user_obj):
        """
            return seconds that user can be online with current conditions
            it may change during the user session because of credit change or login/logout of an instance of user.
            Just useful for showing users.
            return -1 for unlimited time
        """
        return -1

    def commit(self,user_obj): 
        """
            saves all user info (rule usage) from memory into db
        """
        pass
        

#-----------------------------------------------------------------------------------------------------------
class ChargeWithRules(Charge):

    def __init__(self,charge_id,name,comment,admin_id,visible_to_all,_type):
        Charge.__init__(self,charge_id,name,comment,admin_id,visible_to_all,_type)
        self.rules={} #{rule_id=>rule_obj}

    def getRules(self):
        return self.rules
    
    def initUser(self,user_obj):
        Charge.initUser(self,user_obj)

        if user_obj.instances==1: #this is a new user_obj
            if user_obj.initial_credit<=0:
                raise LoginException(errorText("USER_LOGIN","CREDIT_FINISHED"))

            if user_obj.isNormalUser():
                user_obj.charge_info=InternetUserCharge()
            else:
                user_obj.charge_info=VoIPUserCharge()

        user_obj.charge_info.login(user_obj.instances)

        #check if user has an effective rule
        self.getEffectiveRule(user_obj, user_obj.instances) 

    
    def startAccounting(self,user_obj,instance):
        #effectice rule may have been changed
        effective_rule=self.getEffectiveRule(user_obj, instance) 
        user_obj.charge_info.setEffectiveRule(instance, effective_rule)

        Charge.startAccounting(self,user_obj,instance)
        user_obj.charge_info.effective_rules[instance-1].start(user_obj,user_obj.instances)

    def logout(self,user_obj,instance,no_commit):
        """
            no_commit(boolean): don't commit this user data, and just let him go offline
        """
        Charge.logout(self,user_obj,instance)
        if user_obj.charge_info.accounting_started[instance-1]:
            if not no_commit:
                user_obj.charge_info.credit_prev_usage += user_obj.getInstanceInfo(instance)["used_credit"]
            user_obj.charge_info.effective_rules[instance-1].end(user_obj,instance)
        user_obj.charge_info.logout(instance)

    def getEffectiveRule(self,user_obj,instance):
        """
            return currently applicable rule
            
            user_obj (User.User instance):
            instance(integer): instance of user which we want rule for
        """
        return self._getEffectiveRuleForTime(user_obj,instance,time.time())

    def _getEffectiveRuleForTime(self,user_obj,instance,_time):
        """
            return applicable rule for _time
            _time(int): epoch time in seconds
        """     
        max_priority=-1
        max_applicable_rule=None
        
        for rule_id in self.rules:
            rule=self.rules[rule_id]
            if rule.priority > max_priority and rule.appliable(user_obj,instance,_time):
                max_priority=rule.priority
                max_applicable_rule=rule
                
        if max_priority==-1:
            raise LoginException(errorText("USER_LOGIN","NO_APPLICABLE_RULE"))

        return max_applicable_rule
        
    def getNextMoreApplicableRule(self,user_obj, instance):
        """
            return next more applicable rule or None when there's no next more applicable rule
            
            user_obj (User.User instance):
            instance(integer): instance of user which we want rule for
            
        """
        cur_rule=user_obj.charge_info.effective_rules[instance-1]
        return self._getNextMoreApplicableRuleForTime(user_obj, instance, cur_rule, time.time())

    def _getNextMoreApplicableRuleForTime(self,user_obj, instance, cur_rule, _time):
        """
            return next more applicable rule or None when there's no next more applicable rule
            
            user_obj (User.User instance):
            instance(integer): instance of user which we want rule for
            _time(long): seconds from epoch
        """
        
        earliest_more_applicable_rule = None
        secs=secondsFromMorning(_time)
        
        for rule_id in self.rules:
            rule=self.rules[rule_id]
            if rule.interval.containsDay(_time) and rule.interval > secs:
                if rule.priority>cur_rule.priority and rule.anytimeAppliable(user_obj,instance):
                    if earliest_more_applicable_rule==None or earliest_more_applicable_rule.interval > rule.interval:
                        earliest_more_applicable_rule=rule
                
        return earliest_more_applicable_rule


    def calcInstanceCreditUsage(self,user_obj,instance,round_result):
        if not user_obj.charge_info.accounting_started[instance-1]:
            return 0
#       toLog("user_obj.Instances:%s Instance:%s user_obj.charge_info.credit_prev_usage_instance:%s"%(user_obj.instances,instance,user_obj.charge_info.credit_prev_usage_instance),LOG_DEBUG)
        return user_obj.charge_info.credit_prev_usage_instance[instance-1] + self.calcInstanceRuleCreditUsage(user_obj,instance,round_result)

    def calcCreditUsage(self,user_obj,round_result):
        """
            return credit usage amount of user_obj.
            round_result(boolean): Should we round the result with tariff/rule attributes. Rounded result is 
                                   useful for showing and saving while the real amount is needed for calculations
        """
        credit_used=0
        for _index in range(user_obj.instances):
            credit_used+=self.calcInstanceCreditUsage(user_obj,_index+1,round_result)
        return credit_used + user_obj.charge_info.credit_prev_usage
        

    def commit(self,user_obj):
        pass
        
    def __getRule(self,rule_id):
        """
            return rule object with id "rule_id"
        """
        return self.rules[integer(rule_id)]
        
    def setRules(self,rules):
        """
            set rules dic of this charge to rules
            used for loading rules into this charge
        """
        self.rules=rules

    def checkConflict(self,new_charge_rule_obj,ignore_rule_ids=[]):
        """
            check if rules of this charge rule has conflict with "new_charge_rule_obj"
            it'll not check for conflict it rule_ids listed in "ignore_rule_ids"
        """
        for rule_id in self.rules:
            if rule_id not in ignore_rule_ids and self.rules[rule_id].hasOverlap(new_charge_rule_obj):
                raise GeneralException(errorText("CHARGES","RULE_HAS_OVERLAP")%self.rules[rule_id])


    def checkChargeRuleID(self,charge_rule_id):
        """
            check if "charge_rule_id" is valid rule_id in this charge
            raise a generalException if it's not
        """
        if charge_rule_id not in self.rules:
            raise GeneralException(errorText("CHARGES","INVALID_RULE_ID_IN_CHARGE")%(charge_rule_id,self))


    def checkLimits(self,user_obj):
        pass

    def calcInstanceRuleCreditUsage(self,user_obj,instance,round_result):
        pass