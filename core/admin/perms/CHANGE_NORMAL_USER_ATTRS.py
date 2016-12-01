from core.admin.admin_perm import *
from core.admin import perm_loader

def init():
    perm_loader.getLoader().registerPerm("CHANGE NORMAL USER ATTRIBUTES",ChangeNormalUserAttrs)

class ChangeNormalUserAttrs (AllRestrictedSingleValuePermission,UserCatPermission,Permission):
    def init(self):
        self.setDescription(""" Can Change Normal User Attributes
                This Permission Allows admins to add,change or delete users normal attributes
                such as normal username, normal password and normal charge rule
                Normal attributes are commonly used for dialup users
                Related Permissions: ADD NEW USER, CHANGE USER OWNER, CHANGE USER ATTRIBUTES, CHANGE VOIP USER ATTRIBUTES
               """)
        self.addAffectedPage("User->Edit Attributes")
        self.addDependency("CHANGE USER ATTRIBUTES")

    def check(self,admin_obj,admin_perm_obj,user_id,owner_id):
        """
            user_id: id of user we want to check if we can change
            owner_id: owner of user
        """
        if user_id==None and owner_id==None: #group changes
            return

        AllRestrictedSingleValuePermission.check(self, admin_obj, admin_perm_obj, user_id, owner_id)