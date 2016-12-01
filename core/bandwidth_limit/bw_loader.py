from core.ibs_exceptions import *
from core.errors import errorText
from core.bandwidth_limit.node import Node
from core.bandwidth_limit.leaf import LeafService,Leaf
from core.bandwidth_limit.interface import Interface
from core.bandwidth_limit.static_ip import StaticIP
from core.db import db_main

class BWLoader:
    def __init__(self):
        self.__interfaces_id={}
        self.__interfaces_name={}

        self.__nodes_id={}

        self.__leaves_id={}
        self.__leaves_name={}

        self.__static_ips_id={}
        self.__static_ips_ip={}

    def getInterfaceByID(self,interface_id):
        try:
            return self.__interfaces_id[interface_id]
        except KeyError:
            raise GeneralException(errorText("BANDWIDTH","INVALID_INTERFACE_ID")%interface_id)

    def getInterfaceByName(self,interface_name):
        try:
            return self.__interfaces_name[interface_name]
        except KeyError:
            raise GeneralException(errorText("BANDWIDTH","INVALID_INTERFACE_NAME")%interface_name)


    def getNodeByID(self,node_id):
        try:
            return self.__nodes_id[node_id]
        except KeyError:
            raise GeneralException(errorText("BANDWIDTH","INVALID_NODE_ID")%node_id)

    def getLeafByID(self,leaf_id):
        try:
            return self.__leaves_id[leaf_id]
        except KeyError:
            raise GeneralException(errorText("BANDWIDTH","INVALID_LEAF_ID")%leaf_id)

    def getLeafByName(self,leaf_name):
        try:
            return self.__leaves_name[leaf_name]
        except KeyError:
            raise GeneralException(errorText("BANDWIDTH","INVALID_LEAF_NAME")%leaf_name)

    def getStaticIPByID(self,static_ip_id):
        try:
            return self.__static_ips_id[static_ip_id]
        except KeyError:
            raise GeneralException(errorText("BANDWIDTH","INVALID_STATIC_IP_ID")%static_ip_id)

    def getStaticIPByIP(self,static_ip_addr):
        try:
            return self.__static_ips_ip[static_ip_addr]
        except KeyError:
            raise GeneralException(errorText("BANDWIDTH","INVALID_STATIC_IP")%static_ip_addr)
#############################################################
    def loadAll(self):
        interface_ids=self.__getAllInterfaceIDs()
        map(self.loadInterface,interface_ids)
        map(self.loadNodesByInterfaceID,interface_ids)
        map(self.loadLeavesByInterfaceID,interface_ids)
        self.loadAllStaticIPs()

    def __getAllInterfaceIDs(self):
        int_ids_db=self.__getAllInterfaceIDsDB()
        return map(lambda _dic:_dic["interface_id"],int_ids_db) 
    
    def __getAllInterfaceIDsDB(self):
        return db_main.getHandle().get("bw_interface","",0,-1,"interface_id",["interface_id"])
    
    def loadNodesByInterfaceID(self,interface_id):
        node_ids=self.__getNodesWithInterfaceID(interface_id)
        map(self.loadNode,node_ids)

    def __getNodesWithInterfaceID(self,interface_id):
        node_ids_db=db_main.getHandle().get("bw_node","",0,-1,"node_id",["node_id"])
        return map(lambda _dic:_dic["node_id"],node_ids_db)

    def loadLeavesByInterfaceID(self,interface_id):
        leaf_ids=self.__getLeavesWithInterfaceID(interface_id)
        map(self.loadLeaf,leaf_ids)

    def __getLeavesWithInterfaceID(self,interface_id):
        leaf_ids_db=db_main.getHandle().get("bw_leaf","",0,-1,"leaf_id",["leaf_id"])
        return map(lambda _dic:_dic["leaf_id"],leaf_ids_db)

##############################################################
    def interfaceNameExists(self,interface_name):
        return self.__interfaces_name.has_key(interface_name)

    def getAllInterfaceNames(self):
        return self.__interfaces_name.keys()

    def loadInterface(self,interface_id):
        interface_obj=self.__createInterfaceObj(interface_id)
        self.__keepInterfaceObj(interface_obj)

    def unloadInterface(self,interface_id):
        int_obj=self.getInterfaceByID(interface_id)
        del(self.__interfaces_id[interface_id])
        del(self.__interfaces_name[int_obj.getInterfaceName()])
    
    def __keepInterfaceObj(self,interface_obj):
        self.__interfaces_id[interface_obj.getInterfaceID()]=interface_obj
        self.__interfaces_name[interface_obj.getInterfaceName()]=interface_obj

    def __createInterfaceObj(self,interface_id):
        int_info=self.__getInterfaceInfo(interface_id)
        return Interface(int_info["interface_id"],int_info["interface_name"],int_info["comment"])
        
    def __getInterfaceInfo(self,interface_id):
        return db_main.getHandle().get("bw_interface","interface_id=%s"%interface_id)[0]


###############################################################
    def getAllNodeIDs(self):
        return self.__nodes_id.keys()

    def loadNode(self,node_id):
        node_obj=self.__createNodeObj(node_id)
        self.__keepNodeObj(node_obj)

    def unloadNode(self,node_id):
        del(self.__nodes_id[node_id])
    
    def __keepNodeObj(self,node_obj):
        self.__nodes_id[node_obj.getNodeID()]=node_obj

    def __createNodeObj(self,node_id):
        try:
            node_info=self.__getNodeInfoDB(node_id)
        except IndexError:
            raise GeneralException(errorText("BANDWIDTH","NODE_ID_NOT_FOUND")%node_id)

        return Node(node_info["node_id"],node_info["parent_id"],node_info["interface_id"],node_info["rate_kbits"],node_info["ceil_kbits"])
    
    def __getNodeInfoDB(self,node_id):
        return db_main.getHandle().get("bw_node","node_id=%s"%node_id)[0]

    
################################################################
    def leafNameExists(self,leaf_name):
        return self.__leaves_name.has_key(leaf_name)

    def getAllLeafNames(self):
        return self.__leaves_name.keys()

    def loadLeaf(self,leaf_id):
        leaf_obj=self.__createLeafObj(leaf_id)
        self.__keepLeafObj(leaf_obj)
        
    def unloadLeaf(self,leaf_id):
        leaf_obj=self.getLeafByID(leaf_id)
        del(self.__leaves_id[leaf_id])
        del(self.__leaves_name[leaf_obj.getLeafName()])
    
    def __keepLeafObj(self,leaf_obj):
        self.__leaves_id[leaf_obj.getLeafID()]=leaf_obj
        self.__leaves_name[leaf_obj.getLeafName()]=leaf_obj

    def __createLeafObj(self,leaf_id):
        try:
            leaf_info=self.__getLeafInfoDB(leaf_id)
        except IndexError:
            raise GeneralException(errorText("BANDWIDTH","LEAF_ID_NOT_FOUND")%leaf_id)
        services=self.__getleafServicesObjs(leaf_id)
        return Leaf(leaf_info["leaf_id"],
                    leaf_info["leaf_name"],
                    leaf_info["parent_id"],
                    leaf_info["interface_id"],
                    leaf_info["total_rate_kbits"],
                    leaf_info["total_ceil_kbits"],
                    leaf_info["default_rate_kbits"],
                    leaf_info["default_ceil_kbits"],
                    services)

    def __getleafServicesObjs(self,leaf_id):
        services_infos=self.__getLeafServicesDB(leaf_id)
        return map(self.__createLeafServicesObj,services_infos)

    def __createLeafServicesObj(self,service_info):
        return LeafService(service_info["leaf_service_id"],service_info["leaf_id"],service_info["protocol"],service_info["filter"],service_info["rate_kbits"],service_info["ceil_kbits"])
    
    def __getLeafInfoDB(self,leaf_id):
        return db_main.getHandle().get("bw_leaf","leaf_id=%s"%leaf_id)[0]

    def __getLeafServicesDB(self,leaf_id):
        return db_main.getHandle().get("bw_leaf_services","leaf_id=%s"%leaf_id)
    ###########################################################
    def loadAllStaticIPs(self):
        static_ip_ids=self.__getAllStaticIPIDs()
        map(self.loadStaticIP,static_ip_ids)

    def loadStaticIP(self,static_ip_id):
        static_ip_obj=self.__createStaticIPObj(static_ip_id)
        self.__keepStaticIP(static_ip_obj)

    def unloadStaticIP(self,static_ip_id):
        static_ip_obj=self.getStaticIPByID(static_ip_id)
        del(self.__static_ips_id[static_ip_id])
        del(self.__static_ips_ip[static_ip_obj.getIP()])

    def getAllStaticIPs(self):
        return self.__static_ips_ip.keys()

    def runOnAllStaticIPs(self,function):
        """
            function(function instance): function to be called with static_ip_obj as argument
        """
        map(function,self.__static_ips_id.values())


    def __getAllStaticIPIDs(self):
        ids_db=db_main.getHandle().get("bw_static_ip","",0,-1,"bw_static_ip_id",["bw_static_ip_id"])
        return map(lambda x:x["bw_static_ip_id"],ids_db)

    def __keepStaticIP(self,static_ip_obj):
        self.__static_ips_ip[static_ip_obj.getIP()]=static_ip_obj
        self.__static_ips_id[static_ip_obj.getStaticIPID()]=static_ip_obj

    def __createStaticIPObj(self,static_ip_id):
        info=self.__getStaticIPInfo(static_ip_id)
        return StaticIP(info["bw_static_ip_id"],info["ip"],info["transmit_leaf_id"],info["receive_leaf_id"])

    def __getStaticIPInfo(self,static_ip_id):
        return db_main.getHandle().get("bw_static_ip","bw_static_ip_id=%s"%static_ip_id)[0]
        