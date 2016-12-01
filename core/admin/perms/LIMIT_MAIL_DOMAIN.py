from core.admin.admin_perm import *
from core.admin import perm_loader
from core.lib import iplib
from core.errors import errorText


def init():
    perm_loader.getLoader().registerPerm("LIMIT MAIL DOMAIN",LimitMailDomain)

class LimitMailDomain (MultiValuePermission,UserCatPermission,Permission):

    def init(self):
        self.setDescription("""Limit Domains this admin can use for email address of users.
                               Multiple domains are allowed and domains should exactly match
                            """)
        
        
        self.addDependency("CHANGE MAILBOX")    

    def check(self, admin_obj, admin_perm_obj, email_domain):
        if email_domain not in admin_perm_obj.getValue():
            raise PermissionException(errorText("ADMIN","MAIL_DOMAIN_RESTRICTED"))
        

