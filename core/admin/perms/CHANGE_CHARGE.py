from core.admin.admin_perm import *
from core.admin import perm_loader

def init():
    perm_loader.getLoader().registerPerm("CHANGE CHARGE",ChangeCharge)

class ChangeCharge (NoValuePermission,ChargeCatPermission,Permission):
    def init(self):
        self.setDescription("""
                Can Add,Delete and edit charges and charge rules
                This will affect both internet and voip charges

                Related Permissions: ACCESS ALL CHARGES,CHARGE ACCESS
               """)

        self.addDependency("ACCESS ALL CHARGES")
        self.addAffectedPage("Setting->Charge->Charge List")

