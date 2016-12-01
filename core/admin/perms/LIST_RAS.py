from core.admin.admin_perm import *
from core.admin import perm_loader

def init():
    perm_loader.getLoader().registerPerm("LIST RAS",ListRas)

class ListRas (NoValuePermission,RasCatPermission,Permission):
    def init(self):
        self.setDescription("""
                Can See All Active Ras IPs. This is required for many reports and graphs
                Related Permissions: GET RAS INFORMATION, CHANGE RAS
               """)
        self.addAffectedPage("Setting->Ras->Ras List")