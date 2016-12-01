from core.charge.charge import ChargeWithRules
from core.ibs_exceptions import *
from core.errors import errorText
from core.user.can_stay_online_result import CanStayOnlineResult
from core.lib.time_lib import *
import time

CHARGE_DEBUG=False

class VoipCharge(ChargeWithRules): 

    def checkLimits(self,user_obj,before_start_accounting=False):
        """
            Check Limits and return a CanStayOnlineResult
            The remaining time returned is the time until one of instances should be killed
            This works for no-multilogin and multilogin rases
            
            before_start_accounting(boolean): for no-multilogin session, we want to know how much user can talk
                                              before the start accounting. So we should set this to True 
        """
        result=CanStayOnlineResult()

        credit=user_obj.calcCurrentCredit()
        if credit<=0: #now set reasons for all instances to credit finished
            result.setKillForAllInstances(errorText("USER_LOGIN","CREDIT_FINISHED",False),user_obj.instances)
            return result

        start=time.time()

        playing={}
        for instance in range(1,user_obj.instances+1):
            if before_start_accounting or user_obj.charge_info.accounting_started[instance-1]:
                playing[instance]={"call_start_time":user_obj.getTypeObj().getCallStartTime(instance)}
                playing[instance]["call_start_rule"]=self._getEffectiveRuleForTime(user_obj,instance,playing[instance]["call_start_time"])
                playing[instance]["call_start_prefix"]=playing[instance]["call_start_rule"].getPrefixObj(user_obj,instance,not before_start_accounting)

        if CHARGE_DEBUG:
            toLog("Playing Dic: %s"%playing, LOG_DEBUG)
        #playing instances, those who have accounting started
        
        remaining_time = 0
        first_iter = True #is this the first iteration? first iteration is important because it examines current state of user
        break_loop = False
        while not break_loop: #continue until one of instances should be killed
                              #this works well on single login sessions, that we want to know when user should
                              #be killed at start of session
                              #for multi login users, we do the loop just once
            credit_usage_per_second=0
            credit_finish_time=defs.MAXLONG
            earliest_rule_end=defs.MAXLONG
            next_more_applicable=defs.MAXLONG
            free_seconds_end=defs.MAXLONG #if user has free seconds remaining from first rule

            seconds_from_morning=secondsFromMorning(start)

            no_effective_rule=0 #number of instances without effective rule for this iteration

            if CHARGE_DEBUG:
                toLog("Loop Start: %s first_iter: %s remaining_time: %s before_start_accounting=%s"%(start,first_iter,remaining_time, before_start_accounting),LOG_DEBUG)


            for instance in playing.keys():


                try:
                    effective_rule = self._getEffectiveRuleForTime(user_obj,instance,start)
                except LoginException,e:
                    no_effective_rule += 1
                    
                    if first_iter:
                        result.addInstanceToKill(instance,str(e))
                        del(playing[instance])
                    else:
                        break_loop=True
                    continue
        
                if first_iter and not before_start_accounting:
                    #change effective rule
                    cur_rule=user_obj.charge_info.effective_rules[instance-1]
                    if  cur_rule!= effective_rule:

                        cur_rule.end(user_obj, instance)
                        effective_rule.start(user_obj,instance)

                        user_obj.charge_info.setEffectiveRule(instance, effective_rule)

                        
                    
                # if effective_rule ras or port are wildcards
                if effective_rule.priority < 3: 
                    #check if a more applicable rule (ras or ports are specified) 
                    #can be used before this rule ends
                    next_more_applicable_rule=self._getNextMoreApplicableRuleForTime(user_obj, instance, effective_rule, start) 
                    if next_more_applicable_rule!=None:
                        next_more_applicable=min(next_more_applicable_rule.interval.getStartSeconds()-seconds_from_morning,next_more_applicable)
                        
                earliest_rule_end=min(earliest_rule_end,effective_rule.interval.getEndSeconds()-seconds_from_morning+1)
    
                #check free seconds
                if start - playing[instance]["call_start_time"] < playing[instance]["call_start_prefix"].getFreeSeconds():
                    free_seconds_end=min(free_seconds_end,playing[instance]["call_start_prefix"].getFreeSeconds() - (start - playing[instance]["call_start_time"]) )
                else:
                    credit_usage_per_second += effective_rule.getPrefixObj(user_obj,instance,False).getCPM() / 60.0
            #end for

            #if all instances knocked out because of no effective rule
            if not len(playing) or no_effective_rule==len(playing): 
                break

            if credit_usage_per_second:
                credit_finish_time = credit / credit_usage_per_second
                
            next_event = min(earliest_rule_end,next_more_applicable,credit_finish_time,free_seconds_end)

            # we should have at least one increment
            if next_event < 1:
                next_event = 1

                toLog("VoIPCharge:Next Event is zero credit: %s credit_usage_per: %s remaining_time: %s next_event: %s credit_finish_time: %s free_seconds_end: %s earliest_rule_end: %s next_more_applicable: %s seconds_from_morning: %s"% \
                (credit,credit_usage_per_second,remaining_time,next_event,credit_finish_time,free_seconds_end,earliest_rule_end,next_more_applicable,seconds_from_morning) \
                ,LOG_ERROR)
        
            #reduce the temp credit
            if credit_usage_per_second:
                credit -= next_event * credit_usage_per_second
                if credit <= 0:
                    break_loop=True
        
            remaining_time += next_event
            # don't go for more than 1 week, who can talk for one week? ;)
            # this may happen if cpm is 0
            if remaining_time > 7 * 24 * 3600 : 
                break_loop = True

            first_iter = False

            start += next_event

            if CHARGE_DEBUG:
                toLog("Loop End: credit: %s credit_usage_per: %s remaining_time: %s next_event: %s credit_finish_time: %s free_seconds_end: %s earliest_rule_end: %s next_more_applicable: %s seconds_from_morning: %s"% \
                (credit,credit_usage_per_second,remaining_time,next_event,credit_finish_time,free_seconds_end,earliest_rule_end,next_more_applicable,seconds_from_morning) \
                ,LOG_DEBUG)
        
            if not before_start_accounting:
                break_loop=True

    
        #end while
        if int(remaining_time) <= 0 and before_start_accounting:
            raise LoginException(errorText("USER_LOGIN","CREDIT_FINISHED"))
        else:
            result.newRemainingTime(remaining_time)
            return result


    ###########################################################
    def calcInstanceCreditUsage(self,user_obj,instance,round_result):
        """
            check lazy_charge in instance info, if it's set, calc the credit from start to end again
        """
        if not user_obj.charge_info.accounting_started[instance-1]:
            return 0

        instance_info=user_obj.getInstanceInfo(instance)
        if instance_info.has_key("lazy_charge") and not instance_info["lazy_charge"]:
            return self.calcInstanceCreditUsageFromStart(user_obj,instance,round_result)
        else:
            return ChargeWithRules.calcInstanceCreditUsage(self,user_obj,instance,round_result)
                
    def calcInstanceRuleCreditUsage(self,user_obj,instance,round_result):
        """
            calculate and return amount of credit that this instance of user consumed
            during --EFFECTIVE-- rule only
            This is lazy mode of calculating user usage
        """
        now = user_obj.getTypeObj().getCallEndTime(instance)
        effective_rule = user_obj.charge_info.effective_rules[instance-1]
        prefix_obj=effective_rule.getPrefixObj(user_obj,instance)
        
        rule_duration=max(now - user_obj.charge_info.rule_start[instance-1] - user_obj.charge_info.remaining_free_seconds[instance-1],0)
        if rule_duration>0 and round_result:
            min_chargable_duration=prefix_obj.getMinChargableDuration()
            duration = now - user_obj.getTypeObj().getCallStartTime(instance)

            if min_chargable_duration and duration<min_chargable_duration:
                rule_duration += min_chargable_duration-duration
            else:
                round_to=prefix_obj.getRoundTo()
                if round_to:
                    rule_duration += round_to - (duration % round_to)
                
        cpm=prefix_obj.getCPM()

        usage=0
        if cpm>0:
            usage=cpm * rule_duration / 60.0

        return usage

    ##########################################################    
    def calcInstanceCreditUsageFromStart(self,user_obj,instance,round_result):
        """
            calculate instance credit usage from call start_time to now again
            This method is useful for rases that send us the real start accounting time, after user login
            or on user logout. this way we can calculate the correct time
        """
        start_time = user_obj.getTypeObj().getCallStartTime(instance)
        end_time = user_obj.getTypeObj().getCallEndTime(instance)
        duration = end_time - start_time
        effective_rule = self._getEffectiveRuleForTime(user_obj,instance,start_time)
        prefix_obj = effective_rule.getPrefixObj(user_obj,instance,False)

        cur_time = start_time + prefix_obj.getFreeSeconds() #current working time

        credit_usage = 0
        cpm = 0

        while cur_time < end_time:
            try:
                effective_rule = self._getEffectiveRuleForTime(user_obj,instance,cur_time)
            except LoginException:
                logException(LOG_ERROR,"VoIPCharge,calcInstanceCreditUsageFromStart")#shouldn't happen(TM)
                break
            next_event = min(cur_time + effective_rule.interval.getEndSeconds() - secondsFromMorning(cur_time),
                             end_time)
            prefix_obj = effective_rule.getPrefixObj(user_obj,instance,False)
            cpm = prefix_obj.getCPM()
            if cpm > 0:
                credit_usage += cpm * (next_event - cur_time) / 60.0
            
            
            if next_event <= cur_time:
                toLog("calcInstanceCreditUsageFromStart: Cur Time:%s == Next Event:%s for user %s instance %s"%(cur_time,
                                                                                                                next_event,
                                                                                                                str(user_obj),
                                                                                                                instance                                                                                                              
                                                                                                                ), LOG_ERROR)
                next_event = cur_time + 1 #we should have at least one increment
            
            cur_time = next_event
        
        if round_result and duration>0: #cpm and effective_rule have their last value here
            min_chargable_duration=prefix_obj.getMinChargableDuration()
            if min_chargable_duration and duration<min_chargable_duration:
                credit_usage += cpm * (min_chargable_duration - duration) / 60.0
            else:
                round_to=prefix_obj.getRoundTo()
                if round_to:
                    credit_usage += cpm * (round_to - (duration % round_to)) / 60.0

        return credit_usage
    ###########################################################
    def getPrefixObj(self,user_obj,instance):
        return user_obj.charge_info.effective_rules[instance].getPrefixObj(user_obj,instance)
        