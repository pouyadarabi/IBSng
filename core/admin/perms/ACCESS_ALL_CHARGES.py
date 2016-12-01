from core.admin.admin_perm import *
from core.admin import perm_loader

def init():
    perm_loader.getLoader().registerPerm("ACCESS ALL CHARGES",ListAllCharges)

class ListAllCharges (NoValuePermission,ChargeCatPermission,Permission):
    def init(self):
        self.setDescription("""
                Can Access All Visible and NonVisible charges. 
                GOD admins and admins with this permission can see charges even they are not visible
                for all, and charge name is not in CHARGE ACCESS values.
                
                Related Permissions: CHANGE CHARGE,CHARGE ACCESS
               """)

        self.addAffectedPage("Setting->Charge->Charge List")

