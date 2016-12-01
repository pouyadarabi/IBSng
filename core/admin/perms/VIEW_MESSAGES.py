from core.admin.admin_perm import *
from core.admin import perm_loader

def init():
    perm_loader.getLoader().registerPerm("VIEW MESSAGES",ViewMessages)

class ViewMessages (NoValuePermission,MiscCatPermission,Permission):
    def init(self):
        self.setDescription("""
                Can view messages that has been sent by users
               """)

        self.addAffectedPage("Admin->User Messages")
