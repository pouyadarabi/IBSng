"""
    Lock plugin: this plugin implements user locks, so user won't be able to login
    lock has attribute "lock" in database, value can be lock reason, but existence of lock attribute
    means that user is locked
"""
from core.user import user_plugin,user_main,attribute
from core.user.attr_updater import AttrUpdater
from core.user.attr_searcher import AttrSearcher
from core.ibs_exceptions import *
from core.errors import errorText
from core.lib.general import *

attr_handler_name="lock"
def init():
    user_main.getUserPluginManager().register("lock",LockUserPlugin,1)
    user_main.getAttributeManager().registerHandler(LockAttrHandler(),["lock"],["lock"],[])

class LockUserPlugin(user_plugin.UserPlugin): 
    def login(self,args):
        if self.user_obj.getUserAttrs().hasAttr("lock"):
            raise LoginException(errorText("USER_LOGIN","USER_LOCKED"))

        
class LockAttrUpdater(AttrUpdater):

    def changeInit(self,lock_reason):
        self.useGenerateQuery({"lock":lock_reason})

    def deleteInit(self):
        self.useGenerateQuery(["lock"])

class LockAttrSearcher(AttrSearcher):
    def run(self):
        search_helper=self.getSearchHelper()
        user_attrs=search_helper.getTable("user_attrs")
        user_attrs.hasAttrSearch(search_helper,"lock","lock")
        user_attrs.likeStrSearch(search_helper,"lock_reason","lock_reason_op","lock")


class LockAttrHandler(attribute.AttributeHandler):
    def __init__(self):
        attribute.AttributeHandler.__init__(self,attr_handler_name)
        self.registerAttrUpdaterClass(LockAttrUpdater,["lock"])
        self.registerAttrSearcherClass(LockAttrSearcher)
