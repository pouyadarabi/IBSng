from core.admin.admin_perm import *
from core.admin import perm_loader

def init():
    perm_loader.getLoader().registerPerm("CHANGE MAILBOX",ChangeMailbox)

class ChangeMailbox (NoValuePermission,UserCatPermission,Permission):
    def init(self):
        self.setDescription("""
                Can create or delete Mailbox , and set users mailbox quota
               """)

        self.addAffectedPage("User->User Information")
        self.addDependency("CHANGE NORMAL USER ATTRIBUTES")

