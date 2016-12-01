from core.admin.admin_perm import *
from core.admin import perm_loader
from core.errors import errorText

def init():
    perm_loader.getLoader().registerPerm("GET USER INFORMATION",GetUserInformation)

class GetUserInformation (AllRestrictedSingleValuePermission,UserCatPermission,Permission):
    def init(self):
        self.setDescription(""" Can See User Information and attributes
                This Permission Allows admins to see users information such as user_id and credit
                and user attributes such as normal and voip attributes
                Related Permissions: ADD NEW USER, CHANGE USER OWNER, CHANGE USER ATTRIBUTES
               """)
        self.addAffectedPage("User->User Information")

    
    def check(self,admin_obj,admin_perm_obj,loaded_user):
        if admin_perm_obj.getValue()=="Restricted" and loaded_user.getBasicUser().getOwnerObj().getAdminID()!=admin_obj.getAdminID():
            raise PermissionException(errorText("USER","ACCESS_TO_USER_DENIED")%loaded_user.getUserID())

        