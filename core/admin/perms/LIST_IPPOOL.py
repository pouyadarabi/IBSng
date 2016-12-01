from core.admin.admin_perm import *
from core.admin import perm_loader

def init():
    perm_loader.getLoader().registerPerm("LIST IPPOOL",ListIPpool)

class ListIPpool (NoValuePermission,RasCatPermission,Permission):
    def init(self):
        self.setDescription("""
                Can List IP Pool names and see their information.
                This Permission is required if you want to assign ip pools to ras or users
                Related Permissions: CHANGE IPPOOL
               """)

        self.addAffectedPage("Setting->IPpool->IPpool List")

