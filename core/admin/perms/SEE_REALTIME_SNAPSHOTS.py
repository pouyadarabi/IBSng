from core.admin.admin_perm import *
from core.admin import perm_loader
from core.errors import errorText

def init():
    perm_loader.getLoader().registerPerm("SEE REALTIME SNAPSHOTS",SeeRealTimeSnapShots)

class SeeRealTimeSnapShots (NoValuePermission,UserCatPermission,Permission):
    def init(self):
        self.setDescription(""" Can See Real Time Graphs
                This Permission Allows admins to see onlines and banwidth real time grapgs
                Related Permissions: 
                    SEE ONLINE SNAPSHOTS
               """)
        self.addAffectedPage("Report->Real Time Graphs")

        