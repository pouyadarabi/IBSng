from core.admin.admin_perm import *
from core.admin import perm_loader
from core.lib import iplib
from core.errors import errorText


def init():
    perm_loader.getLoader().registerPerm("LIMIT LOGIN ADDR",LimitLoginAddr)

class LimitLoginAddr (MultiValuePermission,AdminCatPermission,Permission):
    def init(self):
        self.setDescription("""Limit ip addresses that admin can login from.
                               If admin has this permission he can only login from ip addresses
                               that is specified in this permission. Value can be in format
                               x.x.x.x (single ip address) or x.x.x.x/y.y.y.y (ip address/netmask)
                            """)
        
        
    def check(self,admin_obj,admin_perm_obj,ip_address):
        for iprange in admin_perm_obj.getValue():
            if iplib.isIPAddrIn(ip_address,iprange):
                return
        raise PermissionException(errorText("ADMIN_LOGIN","ADDRESS_BANNED"))

    def checkNewValue(self,new_val):
        if not iplib.checkIPAddr(new_val):
            self.newValueException(errorText("GENERAL","INVALID_IP_ADDRESS",0)%new_val)