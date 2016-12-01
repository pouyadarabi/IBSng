from core.admin.admin_perm import *
from core.admin import perm_loader

def init():
    perm_loader.getLoader().registerPerm("SEE VOIP TARIFF",SeeVoIPTariff)

class SeeVoIPTariff (NoValuePermission,ChargeCatPermission,Permission):
    def init(self):
        self.setDescription("""
                Can List and See VoIP Tariffs and prefixes
                Related Permissions: CHANGE VOIP TARIFF, CHANGE CHARGE
               """)

        self.addDependency("CHANGE CHARGE")
        self.addAffectedPage("Setting->VoIP Tariff")
