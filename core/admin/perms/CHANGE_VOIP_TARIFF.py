from core.admin.admin_perm import *
from core.admin import perm_loader

def init():
    perm_loader.getLoader().registerPerm("CHANGE VOIP TARIFF",ChangeVoIPTariff)

class ChangeVoIPTariff (NoValuePermission,ChargeCatPermission,Permission):
    def init(self):
        self.setDescription("""
                Can Add,Delete and edit VoIP Tariffs and Prefixes

                Related Permissions: SEE VOIP TARIFF, CHANGE CHARGE
               """)

        self.addDependency("CHANGE CHARGE")
        self.addAffectedPage("Setting->VoIP Tariff")

