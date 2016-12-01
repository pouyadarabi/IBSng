from core.admin.admin_perm import *
from core.admin import perm_loader
from core.errors import errorText

def init():
    perm_loader.getLoader().registerPerm("SEE BW SNAPSHOTS", SeeBwSnapshots)

class SeeBwSnapshots (AllRestrictedSingleValuePermission,UserCatPermission,Permission):
    def init(self):
        self.setDescription(""" Can See User Bandwidth snapshots
                Related Permissions: SEE ONLINE SNAPSHOTS, SEE REALTIME SNAPSHOTS
               """)
        self.addAffectedPage("User->User Information")

    
    def check(self, admin_obj, admin_perm_obj, loaded_user):
        if admin_perm_obj.getValue()=="Restricted" and loaded_user.getBasicUser().getOwnerObj().getAdminID()!=admin_obj.getAdminID():
            raise PermissionException(errorText("USER","ACCESS_TO_USER_DENIED")%loaded_user.getUserID())

        