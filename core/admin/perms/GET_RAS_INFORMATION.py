from core.admin.admin_perm import *
from core.admin import perm_loader

def init():
    perm_loader.getLoader().registerPerm("GET RAS INFORMATION",GetRasInfo)

class GetRasInfo (NoValuePermission,RasCatPermission,Permission):
    def init(self):
        self.setDescription("""
                Can See Rases IP,Type,radius secret, ras ports and attributes. 
                Issue here is radius_secret that only trusted admins should see that.

                Related Permissions: LIST RAS, CHANGE RAS
               """)

        self.addDependency("LIST RAS")  
        self.addAffectedPage("Setting->Ras->Ras List")

