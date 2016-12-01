from core.lib import interval
from core.ras import ras_main
from core.lib.time_lib import secondsFromMorning
import time


class ChargeRule:
    ALL="_ALL_" #string to show all of rases or all of ports

    def __init__(self,rule_id,charge_obj,day_of_weeks,start,end,ras_id,ports):
        self.rule_id=rule_id
        self.charge_obj=charge_obj
        self.day_of_weeks=day_of_weeks
        if ras_id=="'NULL'" or ras_id==None:
            self.ras_id=self.ALL
        else:
            self.ras_id=ras_id
        self.ports=ports
        self.start_time=start
        self.end_time=end
        self.interval=interval.Interval(day_of_weeks,start,end)
        self.priority=self.__calcPriority()



    def getInfo(self):
        """
            return a dictionary of charge rule infos
        """
        if self.ras_id!=self.ALL:
            ras_obj=ras_main.getLoader().getRasByID(self.ras_id)
            ras_ip=ras_obj.getRasIP()
            ras_desc=ras_obj.getRasDesc()
        else:
            ras_ip=self.ALL
            ras_desc=self.ALL

        return {"rule_id":self.rule_id,
                "charge_name":self.charge_obj.getChargeName(),
                "day_of_weeks":self.day_of_weeks.getDayNames(),
                "ras":ras_ip,
                "ras_description":ras_desc,
                "ports":self.ports,
                "start_time":self.start_time,
                "end_time":self.end_time
                }

    def getRuleID(self):
        return self.rule_id

    def setRuleID(self,new_rule_id):
        """
            change self.rule_id to "new_rule_id"
        """
        self.rule_id=new_rule_id

    def getRasID(self):
        return self.ras_id

    def getPorts(self):
        return self.ports

    def getDows(self):
        return self.day_of_weeks

    def __calcPriority(self):
        """
            calculates this rule priority
            return 3 when both ras and port are __not__ wildcards
            2 if ras is __not__ wildcard and port is wildcard
            1 if port is __not__ wildcard and ras is wildcard
            0 if both are wildcards
        """     
    
        ret_val=0
        if self.ras_id!=self.ALL:
            ret_val+=2
        if self.ALL not in self.ports:
            ret_val+=1
        return ret_val

    def __str__(self):
        return "Charge Rule with id %s belongs to charge %s"%(self.rule_id,self.charge_obj.getName())

    def start(self,user_obj,instance):
        """
            called when this rule starts for user_obj
            
            user_obj (User.User instance): object of user that this rule change for
            instance (integer): instance number of user 
        """
        user_obj.charge_info.rule_start[instance-1]=time.time()

    def end(self,user_obj,instance):
        """
            called when this rule ends for user_obj     
            
            user_obj (User.User instance): object of user that this rule change for         
            instance (integer): instance number of user             
        """
        user_obj.charge_info.credit_prev_usage_instance[instance-1]+=self.charge_obj.calcInstanceRuleCreditUsage(user_obj,instance,False)

    def hasOverlap(self,new_charge_rule):
        """
            new_charge_rule (ChargeRule instance): 
        
            check wheter this rule has overlap with new_charge_rule
            return False when there is no overlap and True when overlap found
        
        """

        port_match=False
        if new_charge_rule.ras_id==self.ras_id:
            for port in self.ports:
                if port in new_charge_rule.ports:
                    port_match=True
                    break
                    
            if port_match:
                if self.interval.hasOverlap(new_charge_rule.interval):
                    return True
        return False


    def calcRuleUsage(self,user_obj,instance):
        """
            returns amount of time in seconds this rule has been active for this instance of user
            assuming this rule is the effective rule for this instance
        """
        return time.time()-user_obj.charge_info.rule_start[instance-1]

    def appliable(self,user_obj,instance,_time):
        """
            return False if this rule is not applicable for _time and user_obh
            otherwise returns applicability amount of this rule
        """
	if secondsFromMorning(_time) == 23*3600+59*60+59:
	    _time += 1
	
        if not self.interval.containsTime(_time):
            return False
        return self.anytimeAppliable(user_obj, instance)
        

    def anytimeAppliable(self,user_obj,instance):
        """
            return 0 if this rule is not applicable __anytime __
            otherwise returns applicability amount of this rule
        """
        if self.ras_id==self.ALL and self.ALL in self.ports:
            return True
        
        (ras_id,port)=user_obj.getGlobalUniqueID(instance)
        if self.ras_id==ras_id or self.ras_id==self.ALL:
            if port in self.ports or self.ALL in self.ports:
                return True
        return False
