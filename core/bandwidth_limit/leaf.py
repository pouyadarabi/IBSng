import itertools
import types
from core.bandwidth_limit import bw_main
from core.bandwidth_limit.user_leaf import UserLeaf

class Leaf:
    def __init__(self,leaf_id,leaf_name,parent_id,interface_id,total_rate_kbits,total_ceil_kbits,default_rate_kbits,default_ceil_kbits,services):
        """
            services(list of LeafService Instances): services belongs to this leaf
        """
        self.leaf_id=leaf_id
        self.leaf_name=leaf_name
        self.parent_id=parent_id
        self.interface_id=interface_id
        self.total_rate_kbits=total_rate_kbits
        self.total_ceil_kbits=total_ceil_kbits
        self.default_rate_kbits=default_rate_kbits
        self.default_ceil_kbits=default_ceil_kbits
        self.services=services
        
    def getLeafID(self):
        return self.leaf_id

    def getLeafName(self):
        return self.leaf_name

    def getServices(self):
        return self.services
        
    def getTotalRate(self):
        return self.total_rate_kbits

    def getTotalCeil(self):
        return self.total_ceil_kbits

    def getDefaultRate(self):
        return self.default_rate_kbits

    def getDefaultCeil(self):
        return self.default_ceil_kbits
    #########################
    def getParentNode(self):
        return bw_main.getLoader().getNodeByID(self.getParentNodeID())  

    def getParentNodeID(self):
        return self.parent_id
    ##########################
    def getInterfaceID(self):
        return self.interface_id

    def getInterface(self):
        return bw_main.getLoader().getInterfaceByID(self.getInterfaceID())

    def getInterfaceName(self):
        return self.getInterface().getInterfaceName()
    ###########################
    def createUserLeaf(self,ip_addr,direction):
        return UserLeaf(self,ip_addr,direction)
    ###########################
    def hasService(self,service_tuple):
        """
            check if this leaf has a service with this protocol and filter
            service_tuple(tuple): (protocol,filter)
        """
        for service in self.getServices():
            if service.hasOverLap(service_tuple):
                return True
        return False
    ############################
    def hasServiceID(self,service_id):
        if self.getServiceByID(service_id)!=None:
            return True
        return False
    ###########################
    def getServiceByID(self,service_id):
        for service in self.getServices():
            if service.getLeafServiceID()==service_id:
                return service
        return None
    ###########################
    def registerInParent(self):
        """
            register ourself in parent node
        """
        bw_main.getLoader().getNodeByID(self.getParentNodeID()).registerLeaf(self.getLeafID())

    def unregisterInParent(self):
        """
            unregister ourself in parent node, useful when a leaf has been deleted
        """
        bw_main.getLoader().getNodeByID(self.getParentNodeID()).unregisterLeaf(self.getLeafID())

    ###########################
    def getInfo(self):
        return {"leaf_id":self.getLeafID(),
                "leaf_name":self.getLeafName(),
                "parent_id":self.getParentNodeID(),
                "interface_id":self.getInterfaceID(),
                "interface_name":self.getInterfaceName(),
                "total_rate_kbits":self.getTotalRate(),
                "total_ceil_kbits":self.getTotalCeil(),
                "default_rate_kbits":self.getDefaultRate(),
                "default_ceil_kbits":self.getDefaultCeil(),
                "services":map(lambda service:service.getInfo(),self.getServices())}

#########################################################################################
        
class LeafService:
    def __init__(self,leaf_service_id,leaf_id,protocol,_filter,rate_kbits,ceil_kbits):
        """
            _filter(string): until now, it has two parts, a type and a value
                             type is filter identifier like sport,dport,icmp-type and value
                             is port numbers or icmp type
        """
        self.leaf_service_id=leaf_service_id
        self.leaf_id=leaf_id
        self.protocol=protocol
        self._filter=_filter
        self.rate_kbits=rate_kbits
        self.ceil_kbits=ceil_kbits

    def getRate(self):
        return self.rate_kbits

    def getCeil(self):
        return self.ceil_kbits

    def getProtocol(self):
        return self.protocol
    
    def getFilter(self):
        return self._filter

    def getLeafServiceID(self):
        return self.leaf_service_id

    def getLeafID(self):
        return self.leaf_id

    def getLeafName(self):
        return bw_main.getLoader().getLeafByID(self.getLeafID()).getLeafName()

    def getInfo(self):
        return {"leaf_service_id":self.getLeafServiceID(),
                "filter":self.getFilter(),
                "protocol":self.getProtocol(),
                "rate_kbits":self.getRate(),
                "ceil_kbits":self.getCeil(),
                "leaf_id":self.getLeafID(),
                "leaf_name":self.getLeafName()}


    def hasOverLap(self,other):
        """
            check if this service has overlap with "other" service
            other can be another LeafService Instance or a tuple containing (protocol,filter)
        """
        if type(other) in [types.TupleType,types.ListType]:
            return other[0]==self.getProtocol() and self.__filterHasOverLap(other[1],self.getFilter())
        else:
            return other.getProtocol()==self.getProtocol() and self.__filterHasOverLap(other.getFilter(),self.getFilter())

    def __filterHasOverLap(self,filter1,filter2):
        sp1=filter1.split()
        sp2=filter2.split()
        if sp1[0]!=sp2[0]:
            return False
        ports1=sp1[1].split(",")
        ports2=sp2[1].split(",")
        for port in ports1:
            if port in ports2:
                return True
        return False

#########################################################################################
