from core.user import user_plugin,user_main,attribute
from core.user.attr_updater import AttrUpdater
from core.user.attr_holder import AttrHolder
from core.user.attr_searcher import AttrSearcher
from core.ibs_exceptions import *
from core.errors import errorText
from core.lib.general import *
from core.charge import charge_main

attr_handler_name="normal charge"
def init():
    user_main.getAttributeManager().registerHandler(NormalChargeAttrHandler(),["normal_charge"],["normal_charge"],["normal_charge"])

class NormalChargeAttrHolder(AttrHolder):
    def __init__(self,normal_charge_id):
        self.normal_charge_id=int(normal_charge_id)

    def getParsedDic(self):
        return {"normal_charge":charge_main.getLoader().getChargeByID(self.normal_charge_id).getChargeName()}

class NormalChargeAttrUpdater(AttrUpdater):

    def changeInit(self,normal_charge):
        self.charge_name=normal_charge
        self.useGenerateQuery({"normal_charge":charge_main.getLoader().getChargeByName(self.charge_name).getChargeID()})

    def deleteInit(self):
        self.useGenerateQuery(["normal_charge"])

    def checkInput(self,src,action,dargs):
        if src=="group":
            dargs["admin_obj"].canChangeNormalAttrs(None)
        else:
            map(dargs["admin_obj"].canChangeNormalAttrs,dargs["users"].itervalues())
            
        if hasattr(self,"charge_name"):
            dargs["admin_obj"].canUseCharge(self.charge_name)

            charge_obj=charge_main.getLoader().getChargeByName(self.charge_name)
            if not charge_obj.isInternetCharge():
                raise GeneralException(errorText("USER_ACTIONS","INTERNET_CHARGE_EXPECTED")%charge_obj.getType())


    def genQueryAuditLogPrepareOldValue(self,attr_name, old_value):
        return charge_main.getLoader().getChargeByID(int(old_value)).getChargeName()

    def genQueryAuditLogPrepareNewValue(self,attr_name, new_value):
        return self.charge_name


class NormalChargeAttrSearcher(AttrSearcher):
    def run(self):
        self.exactSearchOnUserAndGroupAttrs("normal_charge","normal_charge",lambda x:charge_main.getLoader().getChargeByName(x).getChargeID())

class NormalChargeAttrHandler(attribute.AttributeHandler):
    def __init__(self):
        attribute.AttributeHandler.__init__(self,attr_handler_name)
        self.registerAttrUpdaterClass(NormalChargeAttrUpdater,["normal_charge"])
        self.registerAttrHolderClass(NormalChargeAttrHolder,["normal_charge"])
        self.registerAttrSearcherClass(NormalChargeAttrSearcher)
