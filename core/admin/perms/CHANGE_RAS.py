from core.admin.admin_perm import *
from core.admin import perm_loader

def init():
    perm_loader.getLoader().registerPerm("CHANGE RAS",ChangeRas)

class ChangeRas (NoValuePermission,RasCatPermission,Permission):
    def init(self):
        self.setDescription("""
                Can Add,Deactive and Reactive rases, and change their attribute and ports.
                This permission is required if admin needs to change ras related settings

                Related Permissions: LIST RAS, GET RAS INFORMATION
               """)

        self.addDependency("LIST RAS","GET RAS INFORMATION")    
        self.addAffectedPage("Setting->Ras->Ras List")

