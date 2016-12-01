from core.user import user_type,user_main
from core.lib.time_lib import *
from core.db import ibs_query
import time

class VoIPUser(user_type.UserType):
    def getLoginTime(self,instance):
        return self.getCallStartTime(instance)

    def getCalledNumber(self,instance):
        """
            return called_number of "instance" of user
            if called_number isn't available(eg. on authentication phase) this will return an empty
            string
        """
        try:
            return self.user_obj.getInstanceInfo(instance)["attrs"]["called_number"]
        except KeyError:
            return ""

    def getCallStartTime(self,instance):
        instance_info=self.user_obj.getInstanceInfo(instance)
        if instance_info.has_key("call_start_time"):
            return instance_info["call_start_time"]
        elif instance_info.has_key("start_accounting"):
            return instance_info["start_accounting"]
        else:
            return instance_info["login_time"]
        
    def getCallEndTime(self,instance):
        instance_info=self.user_obj.getInstanceInfo(instance)
        if instance_info.has_key("call_end_time"):
            return instance_info["call_end_time"]
        else:
            return time.time()
    
    ###########################################
    def logout(self,instance,ras_msg):
        instance_info = self.user_obj.getInstanceInfo(instance)
    
        query=ibs_query.IBSQuery()
        #setup call_start_time and call_end_time
        self.__setTimes(ras_msg,instance_info)
    
        no_commit=False
        if ras_msg.hasAttr("no_commit") and ras_msg["no_commit"]:
            no_commit=True
    
        if no_commit or instance_info.has_key("min_duration") and self.getCallEndTime(instance) - self.getCallStartTime(instance) < instance_info["min_duration"]:
            used_credit=0
            self.user_obj.setKillReason(instance,"Missed Call")
        else:
            used_credit=self.user_obj.charge.calcInstanceCreditUsage(instance,True)

        if instance_info["successful_auth"] and not no_commit:
            query+=self.user_obj.commit(used_credit)
    
        instance_info["used_credit"]=used_credit
        instance_info["no_commit"]=no_commit

        return (query, used_credit)


    def __setTimes(self,ras_msg,instance_info):
        """
            check for connect_time and disconnect_time in ras_msg attribute, and assign
            them to call_start_time and call_end_time in instance_info
        """
        if ras_msg.hasAttr("connect_time"):
            instance_info["call_start_time"] = ras_msg["connect_time"]
            #make charge smart, by using correct call_start_time
            instance_info["lazy_charge"] = False 
            
        if ras_msg.hasAttr("disconnect_time"):
            instance_info["call_end_time"] = ras_msg["disconnect_time"]

    ###################################
    
    def getOnlineReportDic(self,instance):
        online_dic={"voip_username":self.user_obj.getUserAttrs()["voip_username"]}
        instance_info=self.user_obj.getInstanceInfo(instance)

        if instance_info["attrs"].has_key("called_number"):
            online_dic["called_number"]=instance_info["attrs"]["called_number"]
        else:
            online_dic["called_number"]="N/A"

        if instance_info["attrs"].has_key("prefix_name"):
            online_dic["prefix_name"]=instance_info["attrs"]["prefix_name"]
        else:
            online_dic["prefix_name"]="N/A"
        return online_dic    

    ########################################
    def logToConnectionLog(self,instance):
        instance_info=self.user_obj.getInstanceInfo(instance)
        return user_main.getConnectionLogManager().logConnectionQuery(self.user_obj.getUserID(),
                                                               instance_info["used_credit"],
                                                               dbTimeFromEpoch(self.getCallStartTime(instance)),
                                                               dbTimeFromEpoch(self.getCallEndTime(instance)),
                                                               instance_info["successful_auth"],
                                                               "voip",
                                                               instance_info["ras_id"],
                                                               self.__filter(instance,instance_info["attrs"])
                                                              )
    def __filter(self,instance,attrs):
        return attrs

    ###########################################
    def getSingleSessionRemainingTime(self):
        """
            return calculated remaining time of user, for single h323 sessions.
        """
        return self.getRemainingTime(1) #single h323 implies multi_login = False

    def getRemainingTime(self, instance):
        """
            return calculated remaining time of user and instance
        """
        return self.user_obj.getInstanceInfo(instance)["remaining_time"] 

    def getSingleSessionRemainingCredit(self):
        """
            return amount of credit, for single h323 sessions.
            WARNING: this method uses the fact, single h323 session users can't have multiple simulatenous calls
        """
        return self.user_obj.initial_credit
