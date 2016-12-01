from core.server import handler
from core.bandwidth_limit import bw_main
from core.lib.general import *
from core.ibs_exceptions import *
from core.errors import errorText
from core.charge import charge_main
from core.lib.sort import SortedList

class BWHandler(handler.Handler):
    def __init__(self):
        handler.Handler.__init__(self,"bw")
        self.registerHandlerMethod("addInterface")
        self.registerHandlerMethod("addNode")
        self.registerHandlerMethod("addLeaf")
        self.registerHandlerMethod("addLeafService")
        self.registerHandlerMethod("getInterfaces")
        self.registerHandlerMethod("getNodeInfo")
        self.registerHandlerMethod("getLeafInfo")
        self.registerHandlerMethod("getTree")
        self.registerHandlerMethod("delLeafService")
        self.registerHandlerMethod("delNode")
        self.registerHandlerMethod("getAllLeafNames")
        self.registerHandlerMethod("delLeaf")
        self.registerHandlerMethod("delInterface")
        self.registerHandlerMethod("updateInterface")
        self.registerHandlerMethod("updateNode")
        self.registerHandlerMethod("updateLeaf")
        self.registerHandlerMethod("updateLeafService")
        self.registerHandlerMethod("addBwStaticIP")
        self.registerHandlerMethod("updateBwStaticIP")
        self.registerHandlerMethod("delBwStaticIP")
        self.registerHandlerMethod("getAllBwStaticIPs")
        self.registerHandlerMethod("getBwStaticIPInfo")
        self.registerHandlerMethod("getActiveLeaves")
        self.registerHandlerMethod("getLeafCharges")
        
    def addInterface(self,request):
        request.needAuthType(request.ADMIN)
        request.getAuthNameObj().canDo("CHANGE BANDWIDTH MANGER")
        request.checkArgs("interface_name","comment")
        bw_main.getActionsManager().addInterface(request["interface_name"],request["comment"])
        
    ##############################
    def addNode(self,request):
        request.needAuthType(request.ADMIN)
        request.getAuthNameObj().canDo("CHANGE BANDWIDTH MANGER")
        request.checkArgs("interface_name","parent_id","rate_kbits","ceil_kbits")
        bw_main.getActionsManager().addNode(request["interface_name"],
                                            to_int(request["parent_id"],"parent id"),
                                            self.__fixLimitKbits(request["rate_kbits"]),
                                            self.__fixLimitKbits(request["ceil_kbits"]))
        

    ##############################
    def __fixLimitKbits(self,limit_kbits,err_txt_key="INVALID_LIMIT_KBITS"):
        try:
            return int(limit_kbits)
        except ValueError:
            raise GeneralException(errorText("BANDWIDTH",err_txt_key)%limit_kbits)
    ##############################
    def addLeaf(self,request):
        request.needAuthType(request.ADMIN)
        request.getAuthNameObj().canDo("CHANGE BANDWIDTH MANGER")
        request.checkArgs("leaf_name","parent_id","default_rate_kbits","default_ceil_kbits","total_rate_kbits","total_ceil_kbits")
        bw_main.getActionsManager().addLeaf(request["leaf_name"],
                                            to_int(request["parent_id"],"parent id"),
                                            self.__fixLimitKbits(request["default_rate_kbits"]),
                                            self.__fixLimitKbits(request["default_ceil_kbits"]),
                                            self.__fixLimitKbits(request["total_rate_kbits"],"INVALID_TOTAL_LIMIT_KBITS"),
                                            self.__fixLimitKbits(request["total_ceil_kbits"],"INVALID_TOTAL_LIMIT_KBITS"))
    ###############################
    def addLeafService(self,request):
        request.needAuthType(request.ADMIN)
        request.getAuthNameObj().canDo("CHANGE BANDWIDTH MANGER")
        request.checkArgs("leaf_name","protocol","filter","rate_kbits","ceil_kbits")
        bw_main.getActionsManager().addLeafService(request["leaf_name"],
                                            request["protocol"],
                                            request["filter"],
                                            self.__fixLimitKbits(request["rate_kbits"]),
                                            self.__fixLimitKbits(request["ceil_kbits"]))

        
    ###############################
    def getInterfaces(self,request):
        request.needAuthType(request.ADMIN)
        request.getAuthNameObj().canDo("CHANGE BANDWIDTH MANGER")
        infos={}
        for if_name in bw_main.getLoader().getAllInterfaceNames():
            try:
                infos[if_name]=bw_main.getLoader().getInterfaceByName(if_name).getInfo()
            except GeneralException:
                pass

        return infos    
    #################################
    def getNodeInfo(self,request):
        request.needAuthType(request.ADMIN)
        request.getAuthNameObj().canDo("CHANGE BANDWIDTH MANGER")
        request.checkArgs("node_id")
        return bw_main.getLoader().getNodeByID(to_int(request["node_id"],"node id")).getInfo()
    #################################
    def getLeafInfo(self,request):
        request.needAuthType(request.ADMIN)
        request.getAuthNameObj().canDo("CHANGE BANDWIDTH MANGER")
        request.checkArgs("leaf_name")
        return bw_main.getLoader().getLeafByName(request["leaf_name"]).getInfo()
    #################################
    def getTree(self,request):
        request.needAuthType(request.ADMIN)
        request.getAuthNameObj().canDo("CHANGE BANDWIDTH MANGER")
        request.checkArgs("interface_name")
        return bw_main.getActionsManager().getTree(request["interface_name"])
    #################################
    def delLeafService(self,request):
        request.needAuthType(request.ADMIN)
        request.getAuthNameObj().canDo("CHANGE BANDWIDTH MANGER")
        request.checkArgs("leaf_service_id","leaf_name")
        return bw_main.getActionsManager().delLeafService(request["leaf_name"],to_int(request["leaf_service_id"],"leaf service id"))
    #################################
    def delNode(self,request):
        request.needAuthType(request.ADMIN)
        request.getAuthNameObj().canDo("CHANGE BANDWIDTH MANGER")
        request.checkArgs("node_id")
        return bw_main.getActionsManager().delNode(to_int(request["node_id"],"node id"))
    ##################################
    def getAllLeafNames(self,request):
        request.needAuthType(request.ADMIN)
        request.getAuthNameObj().canDo("CHANGE CHARGE")
        return bw_main.getLoader().getAllLeafNames()
    ##################################
    def delLeaf(self,request):
        request.needAuthType(request.ADMIN)
        request.getAuthNameObj().canDo("CHANGE BANDWIDTH MANGER")
        request.checkArgs("leaf_name")
        return bw_main.getActionsManager().delLeaf(request["leaf_name"])
    ##################################
    def delInterface(self,request):
        request.needAuthType(request.ADMIN)
        request.getAuthNameObj().canDo("CHANGE BANDWIDTH MANGER")
        request.checkArgs("interface_name")
        return bw_main.getActionsManager().delInterface(request["interface_name"])
    ###################################
    def updateInterface(self,request):
        request.needAuthType(request.ADMIN)
        request.getAuthNameObj().canDo("CHANGE BANDWIDTH MANGER")
        request.checkArgs("interface_id","interface_name","comment")
        return bw_main.getActionsManager().updateInterface(to_int(request["interface_id"],"interface id"),request["interface_name"],request["comment"])
    ###################################
    def updateNode(self,request):
        request.needAuthType(request.ADMIN)
        request.getAuthNameObj().canDo("CHANGE BANDWIDTH MANGER")
        request.checkArgs("node_id","rate_kbits","ceil_kbits")
        return bw_main.getActionsManager().updateNode(to_int(request["node_id"],"node id"),
                                                      self.__fixLimitKbits(request["rate_kbits"]),
                                                      self.__fixLimitKbits(request["ceil_kbits"]))
    ###################################
    def updateLeaf(self,request):
        request.needAuthType(request.ADMIN)
        request.getAuthNameObj().canDo("CHANGE BANDWIDTH MANGER")
        request.checkArgs("leaf_id","leaf_name","default_rate_kbits","default_ceil_kbits","total_rate_kbits","total_ceil_kbits")
        bw_main.getActionsManager().updateLeaf(to_int(request["leaf_id"],"leaf id"),
                                            request["leaf_name"],
                                            self.__fixLimitKbits(request["default_rate_kbits"]),
                                            self.__fixLimitKbits(request["default_ceil_kbits"]),
                                            self.__fixLimitKbits(request["total_rate_kbits"],"INVALID_TOTAL_LIMIT_KBITS"),
                                            self.__fixLimitKbits(request["total_ceil_kbits"],"INVALID_TOTAL_LIMIT_KBITS"))

    ####################################
    def updateLeafService(self,request):
        request.needAuthType(request.ADMIN)
        request.getAuthNameObj().canDo("CHANGE BANDWIDTH MANGER")
        request.checkArgs("leaf_name","leaf_service_id","protocol","filter","rate_kbits","ceil_kbits")
        bw_main.getActionsManager().updateLeafService(request["leaf_name"],
                                            to_int(request["leaf_service_id"],"leaf service id"),
                                            request["protocol"],
                                            request["filter"],
                                            self.__fixLimitKbits(request["rate_kbits"]),
                                            self.__fixLimitKbits(request["ceil_kbits"]))

    ######################################
    def addBwStaticIP(self,request):
        request.needAuthType(request.ADMIN)
        request.getAuthNameObj().canDo("CHANGE BANDWIDTH MANGER")
        request.checkArgs("ip_addr","tx_leaf_name","rx_leaf_name")
        bw_main.getActionsManager().addBwStaticIP(request["ip_addr"],request["tx_leaf_name"],request["rx_leaf_name"])

    ######################################
    def updateBwStaticIP(self,request):
        request.needAuthType(request.ADMIN)
        request.getAuthNameObj().canDo("CHANGE BANDWIDTH MANGER")
        request.checkArgs("static_ip_id","ip_addr","tx_leaf_name","rx_leaf_name")
        bw_main.getActionsManager().updateBwStaticIP(to_int(request["static_ip_id"],"StaticIP ID"),
                                                  request["ip_addr"],
                                                  request["tx_leaf_name"],
                                                  request["rx_leaf_name"]
                                                  )

    ########################################
    def delBwStaticIP(self,request):
        request.needAuthType(request.ADMIN)
        request.getAuthNameObj().canDo("CHANGE BANDWIDTH MANGER")
        request.checkArgs("ip_addr")
        bw_main.getActionsManager().delBwStaticIP(request["ip_addr"])
    ########################################
    def getAllBwStaticIPs(self,request):
        request.needAuthType(request.ADMIN)
        request.getAuthNameObj().canDo("CHANGE BANDWIDTH MANGER")
        return bw_main.getLoader().getAllStaticIPs()
    
    ########################################
    def getBwStaticIPInfo(self,request):
        request.needAuthType(request.ADMIN)
        request.getAuthNameObj().canDo("CHANGE BANDWIDTH MANGER")
        request.checkArgs("ip_addr")
        return bw_main.getLoader().getStaticIPByIP(request["ip_addr"]).getInfo()
    ########################################
    def getActiveLeaves(self,request):
        request.needAuthType(request.ADMIN)
        request.getAuthNameObj().canDo("CHANGE BANDWIDTH MANGER")
        return bw_main.getManager().getAllUserLeavesInfo()
    ########################################
    def getLeafCharges(self,request):
        """
            return a list of charge_names that "leaf_name" used in
        """
        request.needAuthType(request.ADMIN)
        request.getAuthNameObj().canDo("CHANGE BANDWIDTH MANGER")
        request.checkArgs("leaf_name")
        
        leaf_obj = bw_main.getLoader().getLeafByName(request["leaf_name"])
        charge_names = charge_main.getActionManager().getChargesWithBwLeaf(leaf_obj.getLeafID())

        sorted_charge_names = SortedList(charge_names)
        sorted_charge_names.sort(False)
        return sorted_charge_names.getList()
    