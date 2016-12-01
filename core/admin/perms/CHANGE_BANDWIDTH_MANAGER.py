from core.admin.admin_perm import *
from core.admin import perm_loader

def init():
    perm_loader.getLoader().registerPerm("CHANGE BANDWIDTH MANAGER",ChangeBandwidthManager)

class ChangeBandwidthManager (NoValuePermission,ChargeCatPermission,Permission):
    def init(self):
        self.setDescription("""
                Can Add,Delete and edit Bandwidth manager options
                including interfaces,tree nodes and leaves

                Related Permissions: CHANGE CHARGE
               """)

        self.addDependency("CHANGE CHARGE")
        self.addAffectedPage("Setting->Bandwidth")

