from core.admin.admin_perm import *
from core.admin import perm_loader
def init():
    perm_loader.getLoader().registerPerm("GOD",GOD)

class GOD (NoValuePermission,AdminCatPermission,Permission):
    def __init__(self,name):
        Permission.__init__(self,name)
        self.setDescription("""Admins with GOD Permission, have all positive permissions. 
                            They can do everything, and no restriction (except LIMIT_LOGIN_ADDR) apply to them
                            """)