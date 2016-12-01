from core.admin.admin_perm import *
from core.admin import perm_loader

def init():
    perm_loader.getLoader().registerPerm("POST MESSAGES",PostMessages)

class PostMessages (NoValuePermission,MiscCatPermission,Permission):
    def init(self):
        self.setDescription("""
                Can Post Message to Users
               """)

        self.addAffectedPage("User->User Information")
