from core.admin.admin_perm import *
from core.admin import perm_loader
from core.errors import errorText

def init():
    perm_loader.getLoader().registerPerm("SEE WEB ANALYZER LOGS",SeeWebAnalyzerLogs)

class SeeWebAnalyzerLogs (AllRestrictedSingleValuePermission,UserCatPermission,Permission):
    def init(self):
        self.setDescription(""" Can See Web Analyzer logs
                This Permission Allows admins to see history of websites has been requested by user.
               """)
        self.addAffectedPage("Report->Web Analyzer Logs")

    def check(self,*args):
        pass

        