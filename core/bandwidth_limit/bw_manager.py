import copy
from core.bandwidth_limit import bw_main
from core.ibs_exceptions import *
from core.event import periodic_events

class BWManager:
    def __init__(self):
        self.user_leaves={} #ipaddr=>(Send User Leaf instance,Recv User Leaf instance)
        self.counters={} #interface_name=>{minor_id:(bytes,packets)}

    def applyBwLimit(self,ip_addr,send_leaf_id,recv_leaf_id):
        send_user_leaf=bw_main.getLoader().getLeafByID(send_leaf_id).createUserLeaf(ip_addr,"send")
        recv_user_leaf=bw_main.getLoader().getLeafByID(recv_leaf_id).createUserLeaf(ip_addr,"receive")
        self.__addToLeaves(ip_addr,send_user_leaf,recv_user_leaf)
        send_user_leaf.addToTC()
        recv_user_leaf.addToTC()
        
    def __addToLeaves(self,ip_addr,send_user_leaf,recv_user_leaf):
        if ip_addr in self.user_leaves:
            toLog("ip address %s is already in bw manager user leaves"%ip_addr,LOG_ERROR)
        self.user_leaves[ip_addr]=(send_user_leaf,recv_user_leaf)


    def removeBwLimit(self,ip_addr):
        try:
            send_user_leaf,recv_user_leaf=self.user_leaves[ip_addr]
        except KeyError:
            logException(LOG_ERROR,"ip address %s is not bw manager user leaves")
            return

        send_user_leaf.delFromTC()
        recv_user_leaf.delFromTC()
        del(self.user_leaves[ip_addr])

    ##############################
    def updateCounters(self):
        for int_name in bw_main.getLoader().getAllInterfaceNames():
            self.counters[int_name]=bw_main.getTCRunner().getCounters(int_name)

    def getCounters(self,interface_name,minor_id):
        """
            return tuple of(bytes,packets,rate)
        """
        try:
            return self.counters[interface_name][minor_id]
        except KeyError:
            return (0,0,0)
    ##############################
    def getAllUserLeavesInfo(self):
        """
            return dic of {ip:(send_leaf_info,recv_leaf_info),..}
        """
        infos={}
        leaves=copy.copy(self.user_leaves)
        for ip in leaves:
            infos[ip]=map(lambda uleaf:uleaf.getInfo(),leaves[ip])
        return infos

class UpdateCounters(periodic_events.PeriodicEvent):
    def __init__(self):
        periodic_events.PeriodicEvent.__init__(self,'BwManager Update Counters',10,[],0)
        
    def run(self):
        bw_main.getManager().updateCounters()
        