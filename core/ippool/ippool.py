from core.ibs_exceptions import *
from core.errors import errorText
from core.ippool import ippool_main
import threading
import copy

class IPPoolContainer:
    def __init__(self, all_ips, debug_name):
        self.used = []
        self.free = copy.copy(all_ips)
        self.all_ips = all_ips
        self.debug_name = debug_name
        self.lock=threading.RLock()
    #############################
    def getDebugName(self):
        return self.debug_name

    def getAllIPs(self):
        return self.all_ips

    def getFreeIPs(self):
        return self.free

    def getUsedIPs(self):
        return self.used


    ############################
    def getUsableIP(self):
        """
            return a free ip of our pool and add it to used list.
            raise a IPpoolFullException if all ip's are used and no free ip is available
        """
        ip = None
        self.lock.acquire()
        try:
            try:
                ip = self.free.pop(0)
            except IndexError:
                raise IPpoolFullException(errorText("IPPOOL","NO_FREE_IP")%self.getDebugName())
            self.used.append(ip)
        finally:
            self.lock.release()

        return ip

    #############################



    def setIPInPacket(self, packet):
        """
            set a new ip address in packet, and return the assigned ip
            may raise IPpoolFullException
        """
        if packet!=None:
            ip=self.getUsableIP()
            packet["Framed-IP-Address"]=ip
            packet["Framed-IP-Netmask"]="255.255.255.255"
            return ip


    def useIP(self, ip):
        """
            add specified ip to "used" list and delete it from "free" list
            raise an IPpoolFullException if ip is currently in use by another user
        """
        if self.hasIP(ip): # do we have this ip?
            self.lock.acquire()
            try:
                try:
                    self.free.remove(ip)
                except ValueError:
                    raise IPpoolFullException(errorText("IPPOOL","NO_FREE_IP")%self.getDebugName())
                
                self.used.append(ip)
                
            finally:
                self.lock.release()
    
    def freeIP(self, ip):
        """
            called when an used ip, freed(normally when user that ip was assigned to were logouted)
        """
        self.lock.acquire()
        try:
            try:
                self.used.remove(ip)
            except ValueError:
                toLog("Trying to free ip %s from pool %s while it's not in used list!"%(self.getDebugName(),ip),LOG_ERROR)
                raise GeneralException(errorText("IPPOOL","IP_NOT_IN_USED_POOL")%(ip,self.getDebugName()))

            #if ip hasn't been deleted from ip list while it was in use
            if self.hasIP(ip):
                self.free.append(ip)
        finally:
            self.lock.release()

    #############################

    def hasIP(self,ip):
        """
            return true if ippool has "ip" in its iplist
        """
        return ip in self.all_ips

    def isIPUsed(self,ip):
        """
            return true if ip in ippool is used
        """
        return ip in self.used
    #############################

    def _reload(self,ip_list):
        self.lock.acquire()
        try:
            self.free=filter(lambda ip:ip not in self.used,ip_list)
            self.all_ips = ip_list
        finally:
            self.lock.release()

class IPPool:
    def __init__(self, ippool_id, ippool_name, comment, ip_list):
        """
            ippool_id(integer): id of ippool
            ippool_name(str): name of ippool
            comment(str):
            ip_list(list of str): list of ip addresses belongs to this IPPool
        """
        self.__assignBasicVars(ippool_id,ippool_name,comment)
        self.ip_container = IPPoolContainer(ip_list, ippool_name)
        
    ###################################
    def __assignBasicVars(self,ippool_id,ippool_name,comment):
        self.ippool_id=ippool_id
        self.ippool_name=ippool_name
        self.comment=comment
    
    def getBasicVars(self):
        return [self.ippool_id,self.ippool_name,self.comment]

    ###################################
    def getContainer(self):
        return self.ip_container
    
    def getIPpoolID(self):
        return self.ippool_id

    def getIPpoolName(self):
        return self.ippool_name

    def getInfo(self):
        return {"ippool_id":self.getIPpoolID(),
                "ippool_name":self.getIPpoolName(),
                "comment":self.comment,
                "ip_list":self.getContainer().getAllIPs(),
                "free":self.getContainer().getFreeIPs(),
                "used":self.getContainer().getUsedIPs()
                }
    
    ###################################

    def setIPInPacket(self, packet):
        return self.getContainer().setIPInPacket(packet)

    def useIP(self, ip):
        return self.getContainer().useIP(ip)

    def freeIP(self, ip):
        return self.getContainer().freeIP(ip)

    ###################################
    def hasIP(self, ip):
        return self.getContainer().hasIP(ip)

    def isIPUsed(self, ip):
        return self.getContainer().isIPUsed(ip)

    ###################################
    def _reload(self):
        """
            reload ippool obj, and sync that to db
        """
        new_obj = ippool_main.getLoader().getIPpoolObjByID(self.getIPpoolID())
        apply(self.__assignBasicVars,new_obj.getBasicVars())
        self.getContainer()._reload(new_obj.getContainer().getAllIPs())

