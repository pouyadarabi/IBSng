from core.charge.charge_rule import ChargeRule
from core.bandwidth_limit import simple_bw_limit
from core.bandwidth_limit import bw_main
from core.ibs_exceptions import *
from core.errors import errorText


class InternetChargeRule(ChargeRule):
    def __init__(self,rule_id,charge_obj,cpm,cpk,day_of_weeks,start,end,bandwidth_limit,bw_tx_leaf_id,bw_rx_leaf_id,assumed_kps,ras_id,ports):
        """
            rule_id (integer) : unique id of this rule

            cpm (integer):        Charge Per Minute
            
            cpk (integer):        Charge Per KiloByte

            day_of_weeks (DayOfWeekIntContainer instance): Days Of Week of this rule 

            start (integer):      Rule start time, seconds from 00:00:00

            end (integer):        Rule end Time, seconds from 00:00:00

            bandwidth_limit (integer): bandwidth limit KiloBytes, now useful for lan (vpn) users only
            
            bw_tx_leaf_id (integer): id of leaf, used for bandwidth manager to shape user transmit, 
                                     can be None that means no leaf_id specified
            bw_rx_leaf_id (integer): same as bw_tx_leaf_id but used for user recieve shaping
        
            assumed_kps (integer): assumed (maximum) transfer rate for this rule in KiloBytes per seconds
                                   this is used to determine maximum user transfer rate and the soonest time
                                   that user with this rule can consume a limited amount of allowed transfer 
            
            ras_id (integer):   ras id, this rule will apply to users that login on this ras_id , if set to self.ALL, if there wasn't
                        any exact match for user, this rule will be used

            ports (list): List of ports belongs to ras_id that this rule will apply to. if ras_id matches
                        and port not matched, the total result is not match and we look for another rule or wildcard rule(self.ALL)
                        if Ports is an empty array, it'll be used for all not matched users
        """
        ChargeRule.__init__(self,rule_id,charge_obj,day_of_weeks,start,end,ras_id,ports)
        self.bandwidth_limit=bandwidth_limit
        self.assumed_kps=assumed_kps
        self.cpm=cpm
        self.cpk=cpk
        self.bw_tx_leaf_id=bw_tx_leaf_id
        self.bw_rx_leaf_id=bw_rx_leaf_id

    def __str__(self):
        return "Internet Charge Rule with id %s belongs to charge %s"%(self.rule_id,self.charge_obj.getChargeName())

    def getAssumedKPS(self):
        return self.assumed_kps

    def getInfo(self):
        dic=ChargeRule.getInfo(self)
        dic["type"]="Internet"
        dic["bandwidth_limit"]=self.bandwidth_limit
        dic["assumed_kps"]=self.assumed_kps
        dic["cpm"]=self.cpm
        dic["cpk"]=self.cpk
        if self.bw_tx_leaf_id==None:
            dic["bw_tx_leaf_name"]=''
            dic["bw_rx_leaf_name"]=''
        else:
            dic["bw_tx_leaf_name"]=bw_main.getLoader().getLeafByID(self.bw_tx_leaf_id).getLeafName()
            dic["bw_rx_leaf_name"]=bw_main.getLoader().getLeafByID(self.bw_rx_leaf_id).getLeafName()
        return dic
    
    def start(self,user_obj,instance):
        """
            called when this rule starts for user_obj
            
            user_obj (User.User instance): object of user that this rule change for
            instance (integer): instance number of user 
        """
        ChargeRule.start(self,user_obj,instance)
        user_obj.charge_info.rule_start_inout[instance-1]=user_obj.getTypeObj().getInOutBytes(instance)

        if self.bandwidth_limit>0:
            simple_bw_limit.applyLimitOnUser(user_obj,instance,self.bandwidth_limit)
        self.__applyBwLimit(user_obj,instance,"apply")

    def end(self,user_obj,instance):
        """
            called when this rule ends for user_obj     
            
            user_obj (User.User instance): object of user that this rule change for         
            instance (integer): instance number of user             
        """
        ChargeRule.end(self,user_obj,instance)
        if self.bandwidth_limit>0:
            simple_bw_limit.removeLimitOnUser(user_obj,instance)
        self.__applyBwLimit(user_obj,instance,"remove")

    def calcRuleInOutUsage(self,user_obj,instance):
        """
            returns (in_bytes,out_bytes) usage for this instance of user during this rule
            assuming this rule is the effective rule for this instance
        """
        cur_in_out=user_obj.getTypeObj().getInOutBytes(instance)
        return (cur_in_out[0]-user_obj.charge_info.rule_start_inout[instance-1][0],cur_in_out[1]-user_obj.charge_info.rule_start_inout[instance-1][1])

    def calcRuleTransferUsage(self,user_obj,instance):
        """
            return amount of user transfer in bytes
        """
        cur_rule_inout=self.calcRuleInOutUsage(user_obj,instance)
        return cur_rule_inout[0]+cur_rule_inout[1]
    
    def __applyBwLimit(self,user_obj,instance,action):
        """
            apply bandwidth limit on user, this is seperate from simple bandwidth limit

            user_obj (User.User instance): object of user that we want to apply limit on
            instance (integer): instance number of user 
            action (integer): can be "apply" and "remove"
            
        """
        if self.bw_tx_leaf_id==None and self.bw_rx_leaf_id==None:
            return

        try:
            ip_addr=user_obj.getTypeObj().getClientAddr(instance)
        except GeneralException:
            logException(LOG_ERROR,"Can't apply bandwidth limit on user")
            return

        try:
            if action=="apply":
                bw_main.getManager().applyBwLimit(ip_addr,self.bw_tx_leaf_id,self.bw_rx_leaf_id)
            else:
                bw_main.getManager().removeBwLimit(ip_addr)
        except:
            logException(LOG_ERROR,"Apply Bw Limit")

