from core.script_launcher import launcher_main
from core import defs
from core.ibs_exceptions import *

class MailActions:
    def getMailboxUsage(self, username):
        usage=-1L
        try:
            fd=launcher_main.getLauncher().popen("%smail/mail_usage"%defs.IBS_ADDONS,[username])
            usage=fd.readline()
            fd.close()
            return long(usage)
        except:
            toLog("Can't query user %s mailbox usage: %s"%(username, usage),LOG_DEBUG)
            return -1

    def deleteMailbox(self, username):
        ret = launcher_main.getLauncher().system("%smail/delete_mailbox"%defs.IBS_ADDONS,[username])
        if not ret:
            toLog("deleteMailbox returned non-zero return code %s"%ret,LOG_DEBUG)

    def createMailbox(self, username):
        ret = launcher_main.getLauncher().system("%smail/create_mailbox"%defs.IBS_ADDONS,[username])
        if not ret:
            toLog("createMailbox returned non-zero return code %s"%ret,LOG_DEBUG)
