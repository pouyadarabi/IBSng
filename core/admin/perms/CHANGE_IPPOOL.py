from core.admin.admin_perm import *
from core.admin import perm_loader

def init():
    perm_loader.getLoader().registerPerm("CHANGE IPPOOL",ChangeIPpool)

class ChangeIPpool (NoValuePermission,RasCatPermission,Permission):
    def init(self):
        self.setDescription("""
                Can Add,Delete and change IP pools and add/delete ip's from them
                This Permission Allow admin to see and change ip pools and ip's in them
                ippools can be assigned to ras and users

                Related Permissions: LIST IPPOOL
               """)

        self.addDependency("LIST IPPOOL")
        self.addAffectedPage("Setting->IPpool->IPpool List")

