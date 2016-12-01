from core.user import user_plugin,user_main,attribute
from core.user.attr_updater import AttrUpdater
from core.user.attr_holder import AttrHolder
from core.user.attr_searcher import AttrSearcher
from core.ibs_exceptions import *
from core.errors import errorText
from core.lib.general import *
from core.charge import charge_main

attr_handler_name="voip charge"
def init():
    user_main.getAttributeManager().registerHandler(VoIPChargeAttrHandler(),["voip_charge"],["voip_charge"],["voip_charge"])

class VoIPChargeAttrHolder(AttrHolder):
    def __init__(self,voip_charge_id):
        self.voip_charge_id=int(voip_charge_id)

    def getParsedDic(self):
        return {"voip_charge":charge_main.getLoader().getChargeByID(self.voip_charge_id).getChargeName()}

class VoIPChargeAttrUpdater(AttrUpdater):

    def changeInit(self,voip_charge):
        self.charge_name=voip_charge
        self.useGenerateQuery({"voip_charge":charge_main.getLoader().getChargeByName(self.charge_name).getChargeID()})

    def deleteInit(self):
        self.useGenerateQuery(["voip_charge"])

    def checkInput(self,src,action,dargs):
        if src=="group":
            dargs["admin_obj"].canChangeVoIPAttrs(None)
        else:
            map(dargs["admin_obj"].canChangeVoIPAttrs,dargs["users"].itervalues())
            
        if hasattr(self,"charge_name"): #update
            dargs["admin_obj"].canUseCharge(self.charge_name)
            charge_obj=charge_main.getLoader().getChargeByName(self.charge_name)
            if not charge_obj.isVoIPCharge():
                raise GeneralException(errorText("USER_ACTIONS","VOIP_CHARGE_EXPECTED")%charge_obj.getType())

    def genQueryAuditLogPrepareOldValue(self,attr_name, old_value):
        return charge_main.getLoader().getChargeByID(int(old_value)).getChargeName()

    def genQueryAuditLogPrepareNewValue(self,attr_name, new_value):
        return self.charge_name



class VoIPChargeAttrSearcher(AttrSearcher):
    def run(self):
        self.exactSearchOnUserAndGroupAttrs("voip_charge","voip_charge",lambda x:charge_main.getLoader().getChargeByName(x).getChargeID())

class VoIPChargeAttrHandler(attribute.AttributeHandler):
    def __init__(self):
        attribute.AttributeHandler.__init__(self,attr_handler_name)
        self.registerAttrUpdaterClass(VoIPChargeAttrUpdater,["voip_charge"])
        self.registerAttrHolderClass(VoIPChargeAttrHolder,["voip_charge"])
        self.registerAttrSearcherClass(VoIPChargeAttrSearcher)
