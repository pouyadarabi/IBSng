from core.admin.admin_perm import *
from core.admin import perm_loader

def init():
    perm_loader.getLoader().registerPerm("DELETE ADMIN",DeleteAdmin)

class DeleteAdmin (NoValuePermission,AdminCatPermission,Permission):
    def init(self):
        self.setDescription("""
                Can Delete Other Admins
                Related Permissions: SEE ADMIN INFO, CHANGE ADMIN DEPOSIT , CHANGE PERMISSIONS , CHANGE ADMIN INFO
               """)
        self.addAffectedPage("Admin->Admin Information")
        self.addDependency("SEE ADMIN INFO")
