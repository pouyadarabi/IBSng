from core.server import handler
from core.charge import charge_main,charge_rule
from core.ras import ras_main
from core.lib.general import *
from core.lib.sort import SortedList

class ChargeHandler(handler.Handler):
    def __init__(self):
        handler.Handler.__init__(self,"charge")
        self.registerHandlerMethod("addNewCharge")
        self.registerHandlerMethod("listCharges")
        self.registerHandlerMethod("getChargeInfo")
        self.registerHandlerMethod("updateCharge")
        self.registerHandlerMethod("addInternetChargeRule")
        self.registerHandlerMethod("updateInternetChargeRule")
        self.registerHandlerMethod("listChargeRules")
        self.registerHandlerMethod("delChargeRule")
        self.registerHandlerMethod("delCharge")
        self.registerHandlerMethod("addVoIPChargeRule")
        self.registerHandlerMethod("updateVoIPChargeRule")


        
    def addNewCharge(self,request):
        request.needAuthType(request.ADMIN)
        request.checkArgs("name","comment","charge_type","visible_to_all")
        requester=request.getAuthNameObj()
        requester.canDo("CHANGE CHARGE")
        charge_main.getActionManager().addCharge(request["name"],request["comment"],request["charge_type"],
                                                 requester.getAdminID(),request["visible_to_all"])

    def listCharges(self,request):
        """
            return a list of charge names

            NOTE: this handler take care of admin permissions and return only charges that admin
                  has access to

            type(string,optional): type of charges                
        """
        request.needAuthType(request.ADMIN)
        requester=request.getAuthNameObj()
        charge_names=charge_main.getLoader().getAllChargeNames()

        def filter_func(charge_name):
            if request.has_key("charge_type") and charge_main.getLoader().getChargeByName(charge_name).getType()!=request["charge_type"]:
                return False
            return requester.canUseCharge(charge_name) 
            
        charge_names = filter(filter_func,charge_names)

        sorted_charge_names = SortedList(charge_names)
        sorted_charge_names.sort(False)
        return sorted_charge_names.getList()

    def getChargeInfo(self,request):
        request.needAuthType(request.ADMIN)
        if request.has_key("charge_name"):
            charge_obj=charge_main.getLoader().getChargeByName(request["charge_name"])
        elif request.has_key("charge_id"):
            charge_obj=charge_main.getLoader().getChargeByID(to_int(request["charge_id"],"charge id"))
        else:
            request.raiseIncompleteRequest("charge_name")
        request.getAuthNameObj().canUseCharge(charge_obj.getChargeName())
        return charge_obj.getChargeInfo()


    def updateCharge(self,request):
        request.needAuthType(request.ADMIN)
        request.checkArgs("charge_id","charge_name","comment","visible_to_all")
        requester=request.getAuthNameObj()
        requester.canDo("CHANGE CHARGE")
        charge_main.getActionManager().updateCharge(to_int(request["charge_id"],"charge id"),request["charge_name"],
                                                    request["comment"],request["visible_to_all"])

    def addInternetChargeRule(self,request):
        request.needAuthType(request.ADMIN)
        request.checkArgs("charge_name","rule_start","rule_end","cpm","cpk","assumed_kps","bandwidth_limit_kbytes",
                          "ras","ports","dows","tx_leaf_name","rx_leaf_name")
        request.getAuthNameObj().canDo("CHANGE CHARGE")
        (ras,ports)=self.__checkRasAndPortWildcards(request)

        return charge_main.getActionManager().addInternetChargeRule(request["charge_name"],
                        request["rule_start"],request["rule_end"],
                        request.fixList("dows"),request["cpm"],request["cpk"],request["assumed_kps"],
                        request["bandwidth_limit_kbytes"],request["tx_leaf_name"],request["rx_leaf_name"],ras,ports)

    def updateInternetChargeRule(self,request):
        request.needAuthType(request.ADMIN)
        request.checkArgs("charge_name","charge_rule_id","rule_start","rule_end","cpm","cpk","assumed_kps","bandwidth_limit_kbytes",
                          "ras","ports","dows","tx_leaf_name","rx_leaf_name")
        request.getAuthNameObj().canDo("CHANGE CHARGE")
        (ras,ports)=self.__checkRasAndPortWildcards(request)


        return charge_main.getActionManager().updateInternetChargeRule(request["charge_name"],
                        request["charge_rule_id"],request["rule_start"],request["rule_end"],
                        request.fixList("dows"),request["cpm"],request["cpk"],request["assumed_kps"],
                        request["bandwidth_limit_kbytes"],request["tx_leaf_name"],request["rx_leaf_name"],ras,ports)



    def __checkRasAndPortWildcards(self,request):
        if request["ports"]=="_ALL_":
            ports=[charge_rule.ChargeRule.ALL]
        else:
            ports=requestDicToList(request["ports"])
            
        if request["ras"]=="_ALL_":
            ras=charge_rule.ChargeRule.ALL
        else:
            ras=ras_main.getLoader().getRasByIP(request["ras"]).getRasID()
        
        return (ras,ports)

    def listChargeRules(self,request):
        request.needAuthType(request.ADMIN)
        request.checkArgs("charge_name")
        request.getAuthNameObj().canUseCharge(request["charge_name"])
        charge_rules=charge_main.getLoader().getChargeByName(request["charge_name"]).getRules()
        infos=map(lambda charge_rule_obj:charge_rule_obj.getInfo(),charge_rules.values())
        sorted=SortedList(infos)
        sorted.sortByPostText('["rule_id"]',0)
        return sorted.getList()
        
    def delChargeRule(self,request):
        request.needAuthType(request.ADMIN)
        request.checkArgs("charge_name","charge_rule_id")
        request.getAuthNameObj().canDo("CHANGE CHARGE")
        charge_main.getActionManager().delChargeRule(to_int(request["charge_rule_id"],"charge rule id"),request["charge_name"])

    def delCharge(self,request):
        request.needAuthType(request.ADMIN)
        request.checkArgs("charge_name")
        request.getAuthNameObj().canDo("CHANGE CHARGE")
        charge_main.getActionManager().delCharge(request["charge_name"])

    def addVoIPChargeRule(self,request):
        request.needAuthType(request.ADMIN)
        request.checkArgs("charge_name","rule_start","rule_end","tariff_name","ras","ports","dows")
        request.getAuthNameObj().canDo("CHANGE CHARGE")
        (ras,ports)=self.__checkRasAndPortWildcards(request)

        return charge_main.getActionManager().addVoIPChargeRule(request["charge_name"],
                        request["rule_start"],request["rule_end"],
                        request.fixList("dows"),request["tariff_name"],ras,ports)

    def updateVoIPChargeRule(self,request):
        request.needAuthType(request.ADMIN)
        request.checkArgs("charge_name","charge_rule_id","rule_start","rule_end","tariff_name",
                          "ras","ports","dows")
        request.getAuthNameObj().canDo("CHANGE CHARGE")
        (ras,ports)=self.__checkRasAndPortWildcards(request)
        return charge_main.getActionManager().updateVoIPChargeRule(request["charge_name"],
                        request["charge_rule_id"],request["rule_start"],request["rule_end"],
                        request.fixList("dows"),request["tariff_name"],ras,ports)
        