from core.admin.admin_perm import *
from core.admin import perm_loader

def init():
    perm_loader.getLoader().registerPerm("SEE ADMIN PERMISSIONS",SeeAdminPermissions)

class SeeAdminPermissions (NoValuePermission,AdminCatPermission,Permission):
    def init(self):
        self.setDescription("""
                Can See Other admins Permissions list.
                All Admins can see their own permission list, and with this permission
                they can see other admins permissions
                Related Permissions: CHANGE ADMIN PERMISSIONS , SEE ADMIN INFO
                """)
        self.addDependency("SEE ADMIN INFO")
        self.addAffectedPage("Admin->Admin Permission List")