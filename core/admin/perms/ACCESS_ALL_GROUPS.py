from core.admin.admin_perm import *
from core.admin import perm_loader

def init():
    perm_loader.getLoader().registerPerm("ACCESS ALL GROUPS",AccessAllGroups)

class AccessAllGroups (NoValuePermission,GroupCatPermission,Permission):
    def init(self):
        self.setDescription("""
                Can Access All Groups in IBS
                GOD admins and admins with this permission can see and use all groups
                
                Related Permissions: ADD NEW GROUP,CHANGE GROUP, GROUP ACCESS
               """)

        self.addAffectedPage("Groups->Group List")

