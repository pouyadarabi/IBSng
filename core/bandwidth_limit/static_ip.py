from core.bandwidth_limit import bw_main
from core.lib.IPy import IP

class StaticIP:
    def __init__(self,static_ip_id,ip_addr,tx_leaf_id,rx_leaf_id):
        """
            static_ip_id(int): id of static_ip
            ip_addr(str): ip address. in format x.x.x.x or x.x.x.x/y
            tx_leaf_id(int): id of send leaf
            rx_leaf_id(int): id of receive leaf 
        """
        self.static_ip_id=static_ip_id
        self.ip_addr=ip_addr
        self.tx_leaf_id=tx_leaf_id
        self.rx_leaf_id=rx_leaf_id

        self.ip_obj=IP(ip_addr)

    def getIP(self):
        return self.ip_addr

    def getStaticIPID(self):
        return self.static_ip_id

    def getTxLeafID(self):
        return self.tx_leaf_id
    
    def getTxLeafName(self):
        return bw_main.getLoader().getLeafByID(self.getTxLeafID()).getLeafName()

    def getRxLeafID(self):
        return self.rx_leaf_id
    
    def getRxLeafName(self):
        return bw_main.getLoader().getLeafByID(self.getRxLeafID()).getLeafName()
        
    def getInfo(self):
        return {"static_ip_id":self.getStaticIPID(),
                "ip":self.getIP(),
                "tx_leaf_id":self.getTxLeafID(),
                "tx_leaf_name":self.getTxLeafName(),
                "rx_leaf_id":self.getRxLeafID(),
                "rx_leaf_name":self.getRxLeafName()}


    #######################
    def hasIP(self,ip_addr):
        return ip_addr in self.ip_obj
        
    #######################
    def apply(self):
        bw_main.getManager().applyBwLimit(self.getIP(),self.getTxLeafID(),self.getRxLeafID())

    def remove(self):
        bw_main.getManager().removeBwLimit(self.getIP())
        