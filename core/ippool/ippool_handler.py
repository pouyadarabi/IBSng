from core.server import handler
from core.ippool import ippool_main
from core.lib.sort import SortedList
from core.lib.general import *
from core.lib import multi_strs

class IPpoolHandler(handler.Handler):
    def __init__(self):
        handler.Handler.__init__(self,"ippool")
        self.registerHandlerMethod("addNewIPpool")
        self.registerHandlerMethod("updateIPpool")
        self.registerHandlerMethod("getIPpoolNames")
        self.registerHandlerMethod("getIPpoolInfo")
        self.registerHandlerMethod("deleteIPpool")
        self.registerHandlerMethod("delIPfromPool")
        self.registerHandlerMethod("addIPtoPool")

    def addNewIPpool(self,request):
        request.needAuthType(request.ADMIN)
        request.getAuthNameObj().canDo("CHANGE IPPOOL")
        request.checkArgs("ippool_name","comment")
        ippool_id=ippool_main.getActionsManager().addNewPool(request["ippool_name"],request["comment"])

    def updateIPpool(self,request):
        request.needAuthType(request.ADMIN)
        request.getAuthNameObj().canDo("CHANGE IPPOOL")
        request.checkArgs("ippool_id","ippool_name","comment")
        ippool_id=ippool_main.getActionsManager().updatePool(to_int(request["ippool_id"],"ippool id"),request["ippool_name"],request["comment"])

    def getIPpoolNames(self,request):
        request.needAuthType(request.ADMIN)
        request.getAuthNameObj().canDo("LIST IPPOOL")
        sorted=SortedList(ippool_main.getLoader().getAllIPpoolNames())
        sorted.sort(False)
        return sorted.getList()
    
    def getIPpoolInfo(self,request):
        request.needAuthType(request.ADMIN)
        request.getAuthNameObj().canDo("LIST IPPOOL")
        request.checkArgs("ippool_name")
        return ippool_main.getLoader().getIPpoolByName(request["ippool_name"]).getInfo()
    
    def deleteIPpool(self,request):
        request.needAuthType(request.ADMIN)
        request.getAuthNameObj().canDo("CHANGE IPPOOL")
        request.checkArgs("ippool_name")
        ippool_main.getActionsManager().deletePool(request["ippool_name"])
        
    def delIPfromPool(self,request):
        request.needAuthType(request.ADMIN)
        request.getAuthNameObj().canDo("CHANGE IPPOOL")
        request.checkArgs("ippool_name","ip")
        ippool_main.getActionsManager().delIPfromPool(request["ippool_name"],multi_strs.MultiStr(request["ip"].strip(),False))
    
    def addIPtoPool(self,request):
        request.needAuthType(request.ADMIN)
        request.getAuthNameObj().canDo("CHANGE IPPOOL")
        request.checkArgs("ippool_name","ip")
        ippool_main.getActionsManager().addIPtoPool(request["ippool_name"],multi_strs.MultiStr(request["ip"].strip(),False))

