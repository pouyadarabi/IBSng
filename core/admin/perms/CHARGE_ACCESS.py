from core.admin.admin_perm import *
from core.admin import perm_loader
from core.errors import errorText
from core.charge import charge_main


def init():
    perm_loader.getLoader().registerPerm("CHARGE ACCESS",ChargeAccess)

class ChargeAccess (MultiValuePermission,ChargeCatPermission,Permission):
    def init(self):
        self.setDescription("""
                Can use these charges even they are not visible to all.
                if admin wants to use a charge that is not visible to all ibs checks :
                    1- if admin is GOD => PASS
                    2- if admin has pemission ACCESS ALL CHARGE  => PASS
                    3- if charge is in CHARGE ACCESS values => PASS
                    4- if charge is visible to all => PASS
                    5- FAIL
                
                Related Permissions: ACCESS ALL CHARGES,CHANGE CHARGE
               """)

        self.addAffectedPage("Setting->Charge->Charge List")

    def getValueCandidates(self):
        return charge_main.getLoader().getAllChargeNames()
        
    def check(self,admin_obj,admin_perm_obj,charge_name):
        if charge_name not in admin_perm_obj.getValue():
            raise PermissionException(errorText("CHARGES","ACCESS_TO_CHARGE_DENIED")%charge_name)

    def checkNewValue(self,new_val):
        charge_main.getLoader().checkChargeName(new_val)
