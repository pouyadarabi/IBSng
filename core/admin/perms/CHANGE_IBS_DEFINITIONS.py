from core.admin.admin_perm import *
from core.admin import perm_loader

def init():
    perm_loader.getLoader().registerPerm("CHANGE IBS DEFINITIONS",ChangeIbsDefinitions)

class ChangeIbsDefinitions (NoValuePermission,AdminCatPermission,Permission):
    def init(self):
        self.setDescription("""
                Can see and change IBS definitions. IBS definitions are configurable items that tell ibs how it should
                work. Only System Administrator should have this permission and normal ibs admins/resellers should not have
                access to change this definitions. Example of definitions are radius ports and snmp timeouts
               """)
        self.addAffectedPage("Misc->IBS definitions")
