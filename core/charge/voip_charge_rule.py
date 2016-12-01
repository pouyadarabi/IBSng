from core.charge.charge_rule import ChargeRule
from core.charge.voip_tariff import tariff_main
import time

class VoipChargeRule(ChargeRule): 
    def __init__(self,rule_id,charge_obj,day_of_week,start,end,tariff_id,ras_id,ports):
        """
            rule_id (integer) : unique id of this rule


            day_of_week (integer): Day Of Week of this rule 

            start (integer):      Rule start time, seconds from 00:00:00

            end (integer):        Rule end Time, seconds from 00:00:00
            
            tariff_id (integer): tariff list which we try to find cpm from
            
            ras_id (integer):   ras id, this rule will apply to users that login on this ras_id , if set to None, if there wasn't
                        any exact match for user, this rule will be used

            ports (list): List of ports belongs to ras_id that this rule will apply to. if ras_id matches
                        and port not matched, the total result is not match and we look for another rule or wildcard rule(None)
                        if Ports is an empty array, it'll be used for all not matched users
        """
        ChargeRule.__init__(self,rule_id,charge_obj,day_of_week,start,end,ras_id,ports)
        self.tariff_id=tariff_id

    def __str__(self):
        return "VoIP Charge Rule with id %s belongs to charge %s"%(self.rule_id,self.charge_obj.getChargeName())

    ######################################
    def start(self,user_obj,instance):
        """
            called when this rule starts for user_obj
            
            user_obj (User.User instance): object of user that this rule change for
            instance (integer): instance number of user 
        """
        ChargeRule.start(self,user_obj,instance)
        prefix_obj=self.getPrefixObj(user_obj,instance,False)
        user_obj.charge_info.prefix_id[instance-1]=prefix_obj.getPrefixID()
        if user_obj.charge_info.remaining_free_seconds[instance-1]==-1:#we're the first rule of this instance
            user_obj.charge_info.remaining_free_seconds[instance-1]=prefix_obj.getFreeSeconds()
            instance_info=user_obj.getInstanceInfo(instance)
            instance_info["min_duration"]=prefix_obj.getMinDuration()
            instance_info["attrs"]["prefix_name"]=prefix_obj.getPrefixName()


    #####################################
    def end(self,user_obj,instance):
        """
            called when this rule ends for user_obj     
            
            user_obj (User.User instance): object of user that this rule change for         
            instance (integer): instance number of user             
        """
        ChargeRule.end(self,user_obj,instance)
        rule_duration=time.time() - user_obj.charge_info.rule_start[instance-1]
        if rule_duration>user_obj.charge_info.remaining_free_seconds[instance-1]:
            user_obj.charge_info.remaining_free_seconds[instance-1]=0
        else:
            user_obj.charge_info.remaining_free_seconds[instance-1]-=rule_duration

    #####################################
    def getTariffObj(self):
        return tariff_main.getLoader().getTariffByID(self.tariff_id)
        
    #####################################
    def getPrefixObj(self,user_obj,instance,cur_rule=True):
        """
            return prefix_obj for "instance" of  "user_obj"
            cur_rule tells if we are the current rule for user
        """
        if cur_rule:
            return self.getTariffObj().getPrefixByID(user_obj.charge_info.prefix_id[instance-1])
        else:
            return self.getTariffObj().findPrefix( \
                                        user_obj.getTypeObj().getCalledNumber(instance))

    #####################################
    def hasPrefixFor(self,called_number):
        """
            return True if this rule has prefix for "called_number"
        """
        return self.getTariffObj().findPrefix(called_number)!=None

    ######################################
    def anytimeAppliable(self,user_obj,instance):
        called_number = user_obj.getTypeObj().getCalledNumber(instance)
        if called_number != "":
            has_prefix = self.hasPrefixFor(called_number)
        else: #we didn't acquire user dialed number yet
            has_prefix = True
            
        return has_prefix and ChargeRule.anytimeAppliable(self,user_obj,instance) 

    ######################################
    def getInfo(self):
        dic=ChargeRule.getInfo(self)
        dic["type"]="VoIP"
        dic["tariff_id"]=self.tariff_id
        dic["tariff_name"]=self.getTariffObj().getTariffName()
        return dic
        