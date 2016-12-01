from core.bandwidth_limit.idpool import IDPool
from core.bandwidth_limit import bw_main

class Interface:
    def __init__(self,interface_id,interface_name,comment):
        self.interface_id=interface_id
        self.interface_name=interface_name
        self.comment=comment
        self.root_node_id=None
        self.minor_id_pool=IDPool((10,0xffff),"interface %s minors"%self.getInterfaceName())
        self.major_id_pool=IDPool((10,0xffff),"interface %s majors"%self.getInterfaceName())

    def getInterfaceID(self):
        return self.interface_id

    def getInterfaceName(self):
        return self.interface_name    
###################
    def getRootNode(self):
        root_node_id=self.getRootNodeID()
        if root_node_id!=None:
            return bw_main.getLoader().getNodeByID(root_node_id)
        else:
            return None

    def getRootNodeID(self):
        return self.root_node_id
###################
    def registerRootNode(self,root_node_id):
        self.root_node_id=root_node_id

    def unregisterRootNode(self,root_node_id):
        self.root_node_id=None
###################
    def addRootQdisc(self):
        bw_main.getTCRunner().delQdisc(self.interface_name,"root")
        bw_main.getTCRunner().addQdisc(self.interface_name,"handle 1:","root","htb")

    def createTree(self):
        self.addRootQdisc()
        self.getRootNode().createSubTree()

###################
    def getMinorIDPool(self):
        return self.minor_id_pool

    def getMajorIDPool(self):
        return self.major_id_pool
#####################
    def getInfo(self):
        return {"interface_id":self.getInterfaceID(),
                "interface_name":self.getInterfaceName(),
                "comment":self.comment}
#####################
    def changeComment(self,comment):
        self.comment=comment
        