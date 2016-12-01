from core.user import user_plugin,user_main,attribute
from core.charge import charge_main
from core.errors import *
from core.ibs_exceptions import *
import time

def init():
    user_main.getUserPluginManager().register("charge",ChargeUserPlugin,6)
    
class ChargeUserPlugin(user_plugin.UserPlugin):
    def __init__(self,user_obj):
        user_plugin.UserPlugin.__init__(self,user_obj)
        self.charge_defined=True
        self.charge_initialized=0 #number of instances with initialized charge
        try:
            if user_obj.isNormalUser():
                self.charge_id=int(user_obj.getUserAttrs()["normal_charge"])
            elif user_obj.isVoIPUser():
                self.charge_id=int(user_obj.getUserAttrs()["voip_charge"])
                    
        except GeneralException:
            self.charge_defined=False
            
        if self.charge_defined:
            self.charge_obj=charge_main.getLoader().getChargeByID(self.charge_id)

 
    def login(self,ras_msg):
        if not self.charge_defined:
            raise GeneralException(errorText("USER_LOGIN","NO_CHARGE_DEFINED")%self.user_obj.getType())

        if ras_msg.hasAttr("called_number"):
            self.__setCalledNumber(ras_msg)
        
        self.__initCharge()

        self.__setRemainingTime(ras_msg)

        if ras_msg.hasAttr("start_accounting"):
            self.__startAccounting(ras_msg)

    def __initCharge(self):
        self.charge_obj.initUser(self.user_obj)
        self.charge_initialized+=1
        
    def __startAccounting(self,ras_msg):
        instance=self.user_obj.getInstanceFromRasMsg(ras_msg)
        self.charge_obj.startAccounting(self.user_obj,instance)
        self.user_obj.getInstanceInfo(instance)["start_accounting"]=time.time()

    def __setCalledNumber(self,ras_msg):
        instance=self.user_obj.getInstanceFromRasMsg(ras_msg)
        if not ras_msg["called_number"]:
            raise LoginException(errorText("USER_LOGIN","INVALID_CALLED_NUMBER"))
        self.user_obj.getInstanceInfo(instance)["attrs"]["called_number"]=ras_msg["called_number"]


    def __setRemainingTime(self, ras_msg):
        instance=self.user_obj.getInstanceFromRasMsg(ras_msg)
        if ras_msg.hasAttr("called_number") and ras_msg.hasAttr("calc_remaining_time") and ras_msg.getAction()=="VOIP_AUTHORIZE":
            self.user_obj.getInstanceInfo(instance)["remaining_time"] = \
                self.getChargeObj().checkLimits(self.user_obj,True).getRemainingTime()


    def update(self,ras_msg):

        if "called_number" in ras_msg["update_attrs"]:
            self.__setCalledNumber(ras_msg)

        if ras_msg.hasAttr("start_accounting"):
            self.__startAccounting(ras_msg)
            return True

    def logout(self,instance,ras_msg):
        if instance<=self.charge_initialized:

            self.charge_obj.logout(self.user_obj,instance,self.user_obj.getInstanceInfo(instance)["no_commit"])
            self.charge_initialized-=1

    def canStayOnline(self):
        if self.charge_initialized:
            return self.charge_obj.checkLimits(self.user_obj)

    def calcCreditUsage(self,round_result):
        if self.charge_initialized:
            return self.charge_obj.calcCreditUsage(self.user_obj,round_result)
        return 0

    def calcInstanceCreditUsage(self,instance,round_result):
        if instance<=self.charge_initialized:
            return self.charge_obj.calcInstanceCreditUsage(self.user_obj,instance,round_result)
        return 0

    def getChargeObj(self):
        return self.charge_obj
        