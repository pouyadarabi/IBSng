from core.server import handler
from core.lib import multi_strs
from core.charge.voip_tariff import tariff_main
from core.lib.sort import SortedList
from core.lib.general import *


class TariffHandler(handler.Handler):
    def __init__(self):
        handler.Handler.__init__(self,"voip_tariff")
        self.registerHandlerMethod("addNewTariff")
        self.registerHandlerMethod("updateTariff")
        self.registerHandlerMethod("deleteTariff")
        self.registerHandlerMethod("addPrefix")
        self.registerHandlerMethod("updatePrefix")
        self.registerHandlerMethod("deletePrefix")
        self.registerHandlerMethod("getTariffInfo")
        self.registerHandlerMethod("listTariffs")


    def addNewTariff(self,request):
        request.needAuthType(request.ADMIN)
        request.getAuthNameObj().canDo("CHANGE VOIP TARIFF")
        request.checkArgs("tariff_name","comment")
        tariff_id=tariff_main.getActionsManager().addNewTariff(request["tariff_name"],request["comment"])
        return tariff_id

    def updateTariff(self,request):
        request.needAuthType(request.ADMIN)
        request.getAuthNameObj().canDo("CHANGE VOIP TARIFF")
        request.checkArgs("tariff_id","tariff_name","comment")
        tariff_main.getActionsManager().updateTariff(to_int(request["tariff_id"],"Tariff id"),request["tariff_name"],request["comment"])

    def deleteTariff(self,request):
        request.needAuthType(request.ADMIN)
        request.getAuthNameObj().canDo("CHANGE VOIP TARIFF")
        request.checkArgs("tariff_name")
        tariff_main.getActionsManager().deleteTariff(request["tariff_name"])

    def addPrefix(self,request):
        request.needAuthType(request.ADMIN)
        request.getAuthNameObj().canDo("CHANGE VOIP TARIFF")
        request.checkArgs("tariff_name","prefix_codes","prefix_names","cpms","free_seconds","min_durations","round_tos","min_chargable_durations")
        return tariff_main.getActionsManager().addPrefix(request["tariff_name"],
                                                  request.fixList("prefix_codes"),
                                                  request.fixList("prefix_names"),
                                                  request.fixList("cpms"),
                                                  request.fixList("free_seconds"),
                                                  request.fixList("min_durations"),
                                                  request.fixList("round_tos"),
                                                  request.fixList("min_chargable_durations"))
        
    def updatePrefix(self,request):
        request.needAuthType(request.ADMIN)
        request.getAuthNameObj().canDo("CHANGE VOIP TARIFF")
        request.checkArgs("tariff_name","prefix_id","prefix_code","prefix_name","cpm","free_seconds","min_duration","round_to","min_chargable_duration")
        tariff_main.getActionsManager().updatePrefix(request["tariff_name"],
                                                  to_int(request["prefix_id"],"prefix id"),
                                                  request["prefix_code"],
                                                  request["prefix_name"],
                                                  to_float(request["cpm"],"cpm"),
                                                  to_int(request["free_seconds"],"free seconds"),
                                                  to_int(request["min_duration"],"min duration"),
                                                  to_int(request["round_to"],"round to"),
                                                  to_int(request["min_chargable_duration"],"min chargable duration"))
        
            
    def deletePrefix(self,request):
        request.needAuthType(request.ADMIN)
        request.getAuthNameObj().canDo("CHANGE VOIP TARIFF")
        request.checkArgs("tariff_name","prefix_code")
        tariff_main.getActionsManager().deletePrefix(request["tariff_name"],multi_strs.MultiStr(request["prefix_code"]))

    def getTariffInfo(self,request):
        """
            return informations of voip tariff, including prefixes if selected
        """
        request.needAuthType(request.ADMIN)
        request.getAuthNameObj().canDo("SEE VOIP TARIFF")
        request.checkArgs("tariff_name","include_prefixes","name_regex")
        return tariff_main.getLoader().getTariffByName(request["tariff_name"]).getInfo(request["include_prefixes"],request["name_regex"])

    def listTariffs(self,request):
        """
            return a list of tariff infos in format [{"tariff_name":,"tariff_id":,"comment":}]
            note that prefixes aren't included
        """
        request.needAuthType(request.ADMIN)
        request.getAuthNameObj().canDo("SEE VOIP TARIFF")
        tariffs=map(lambda tariff_name:tariff_main.getLoader().getTariffByName(tariff_name).getInfo(),
                   tariff_main.getLoader().getAllTariffNames())
        sorted=SortedList(tariffs)
        sorted.sortByValueDicKey("tariff_name",False)
        return sorted.getList()
        
