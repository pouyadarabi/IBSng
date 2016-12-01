from core.ibs_exceptions import *
from core.lib import iplib

DEBUG = False

import threading

class IPMap:
    def __init__(self):
        self.__map={} #ip=>user_id

    def addIP(self, ip_addr, user_id):
        """
            add mapping from "ip_addr" to "user_id"
        """
        if DEBUG:
            toLog("IPMAP: addIP, ip_addr: %s, id: %s, all_ips: %s"%(ip_addr, user_id, iplib.getAllIPs(ip_addr)), LOG_DEBUG)
        
        for ip in iplib.getAllIPs(ip_addr):
            self.__map[ip]=user_id
        
        
    def removeIP(self, ip_addr):
        """
            remove ip from mapping
        """
        try:
            del(self.__map[ip_addr])
        except KeyError:
            toLog("IPMap: Trying remove ip %s while it isn't in list"%ip_addr,LOG_DEBUG)

    def getUserIDForIP(self, ip):
        if DEBUG:
            toLog("IPMAP: getUserIDForIP, ip: %s"%ip, LOG_DEBUG)
        try:
            return self.__map[ip]
        except KeyError:
            return None
