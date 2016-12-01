from core.user import user_plugin,user_main,attribute
from core.user.attr_updater import AttrUpdater
from core.user.attr_searcher import AttrSearcher
from core.ibs_exceptions import *
from core.errors import errorText
from core.lib.general import *

def init():
    user_main.getAttributeManager().registerHandler(MailQuotaAttrHandler(),["mail_quota"],["mail_quota"],[],[calcMailboxUsage])


def calcMailboxUsage(_id,_type,raw_attrs,parsed_attrs,date_type):
    if _type!="user":
        return

    if raw_attrs.has_key("mail_quota") and raw_attrs.has_key("email_address"):
        parsed_attrs["mail_usage"]=user_main.getMailActions().getMailboxUsage(raw_attrs["email_address"])
        
class MailQuotaAttrUpdater(AttrUpdater):
    def checkInput(self,src,action,dargs):
        if src=="user":
            map(dargs["admin_obj"].canChangeNormalAttrs,dargs["users"].itervalues())
        else:
            dargs["admin_obj"].canChangeNormalAttrs(None)
        
        dargs["admin_obj"].canDo("CHANGE MAILBOX")

    def changeInit(self,mail_quota):
        try:
            mail_quota=int(mail_quota)
        except ValueError:
            raise GeneralException(errorText("USER_ACTIONS","MAIL_QUOTA_NOT_INTEGER"))
        
        if mail_quota<=0:
            raise GeneralException(errorText("USER_ACTIONS","MAIL_QUOTA_NOT_INTEGER"))

        self.useGenerateQuery({"mail_quota":mail_quota})

    def deleteInit(self):
        self.useGenerateQuery(["mail_quota"])

class MailQuotaAttrSearcher(AttrSearcher):
    def run(self):
        search_helper=self.getSearchHelper()
        user_attrs=search_helper.getTable("user_attrs")
        user_attrs.ltgtSearch(search_helper,"mail_quota","mail_quota_op","mail_quota")


class MailQuotaAttrHandler(attribute.AttributeHandler):
    def __init__(self):
        attribute.AttributeHandler.__init__(self,"mail_quota")
        self.registerAttrUpdaterClass(MailQuotaAttrUpdater,["mail_quota"])
        self.registerAttrSearcherClass(MailQuotaAttrSearcher)
