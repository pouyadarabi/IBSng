from core.admin.admin_perm import *
from core.admin import perm_loader

def init():
    perm_loader.getLoader().registerPerm("DELETE REPORTS",DeleteReports)

class DeleteReports (NoValuePermission,MiscCatPermission,Permission):
    def init(self):
        self.setDescription("""
                Can Delete and Clean Reports of IBS
                With deleting a report, it isn't accessible any more, so reports should be deleted 
                only when they aren't needed anymore.
                This Permission should be given only to highly trusted admins. Miss use of this
                feature can lead to deleting important data from IBS.
               """)
        self.addAffectedPage("Setting->Clean Report")