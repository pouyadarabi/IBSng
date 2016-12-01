from core.admin.admin_perm import *
from core.admin import perm_loader
from core.errors import errorText

def init():
    perm_loader.getLoader().registerPerm("SEE ONLINE SNAPSHOTS",SeeOnlineSnapShots)

class SeeOnlineSnapShots (NoValuePermission,UserCatPermission,Permission):
    def init(self):
        self.setDescription(""" Can See Online count Graphs
                This Permission Allows admins to see online count of specific date
                Related Permissions: 
                    SEE REALTIME SNAPSHOTS
               """)
        self.addAffectedPage("Report->Online Graphs")

        