from core.admin.admin_perm import *
from core.admin import perm_loader

def init():
    perm_loader.getLoader().registerPerm("CHANGE ADMIN PERMISSIONS",ChangeAdminPermissions)

class ChangeAdminPermissions (NoValuePermission,AdminCatPermission,Permission):
    def init(self):
        self.setDescription("""
                Can add or  delete permissions from  permissions from admins or Change 
                Admin Permission's value.
                Owner of this permission can change his own permissions too, so this permission
                is somehow equivalent to GOD and should given to trusted admins only
                Related Permissions: SEE ADMIN PERMISSIONS , SEE ADMIN INFO, GOD
                """)
        self.addDependency("SEE ADMIN INFO","SEE ADMIN PERMISSIONS")
        self.addAffectedPage("Admin->Admin Permission List","Admin->Add Permission To Admin")