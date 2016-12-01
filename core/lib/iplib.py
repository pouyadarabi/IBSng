"""
    some wrappers for IPy, use IPy directly if you need more complete API
"""

from core.lib import IPy
from core import defs
from core.errors import errorText

def isIPAddrIn(ip_addr,ip_addrrange):
    """
        check if addr is in addrrange
        return true if it is, and false if it's not
    """
    try:
        ip=IPy.IP(ip_addr)
        iprange=IPy.IP(ip_addrrange)
        if ip in iprange:
            return True
        return False
    except:
        logException(LOG_ERROR,"isIPAddrIn")
        raise GeneralException(errorText("GENERAL","INVALID_IP_ADDRESS")%ip_addr)


def checkIPAddr(ip_addr):
    """
        check ip_addr if it's valid, it can be in format x.x.x.x or x.x.x.x/y.y.y.y
        in case of ip/netmask netmask is checked for validity too
        return 1 if it's valid and 0 if it's not
    """
    try:
        ip=IPy.IP(ip_addr)
        return True
    except:
        return False

def checkIPAddrWithoutMask(addr):
    if addr.find("/")!=-1:
        return False
    if len(addr.split('.')) != 4:
        return False
    try:
        ip=IPy.IP(addr)
        return True
    except:
        return False


def formatIPAddress(ip_addr):
    """
        Make sure ip address has the format ip/bitwise_netmask
        return the formatted ip address
        
    """
    ip=IPy.IP(ip_addr)
    ip.NoPrefixForSingleIp=False
    return str(ip)

def getAllIPs(ip_addr):
    """
        return a list of all ips in ip_addr. if ip_addr includes netmask, return all included ips
    """
    if ip_addr.find("/")==-1:
        return [ip_addr]
    else:
        return map(str,IPy.IP(ip_addr))

#########################################
class IP:
    def __init__(self, ip):
        """
            ip(str): ip or ip/netmask
        """
        self.ip=ip
        if self.ip.find("/")!=-1:
            self.has_netmask=True
            self.ip_obj=IPy.IP(self.ip)
        else:
            self.has_netmask=False
            self.ip_obj=None

    def __eq__(self, ip):
        """
            check if "ip" is equals or --included-- in this IP Address
        """
        if self.has_netmask:
            return ip in self.ip_obj
        else:
            return ip == self.ip        
