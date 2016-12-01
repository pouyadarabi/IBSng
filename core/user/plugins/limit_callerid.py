"""
    Limit CallerID Plugin: This plugin limit caller id that user can login from
"""
from core.user import user_plugin,user_main,attribute
from core.user.attr_updater import AttrUpdater
from core.user.attr_searcher import AttrSearcher
from core.ibs_exceptions import *
from core.errors import errorText
from core.lib.general import *
from core.lib.multi_strs import MultiStr
from core.lib import maclib
import re


attr_handler_name="limit_caller_id"
def init():
    user_main.getUserPluginManager().register("limit_caller_id",LimitCallerIDPlugin,1)
    user_main.getAttributeManager().registerHandler(LimitCallerIDAttrHandler(),["limit_caller_id"],["limit_caller_id"],[])

class LimitCallerIDPlugin(user_plugin.AttrCheckUserPlugin):
    def __init__(self,user_obj):
        user_plugin.AttrCheckUserPlugin.__init__(self,user_obj,"limit_caller_id")
        self.__initValues()

    def __initValues(self):
        if self.hasAttr():
            self.caller_id_patterns = map(
                                        re.compile,MultiStr(self.user_obj.getUserAttrs()["limit_caller_id"]))
            self.allow_no_caller_id = self.user_obj.getUserAttrs()["limit_caller_id_allow_not_defined"] == "1"

    def s_login(self,ras_msg):
        if ras_msg.hasAttr("caller_id"):
            for pattern in self.caller_id_patterns:
                if pattern.search(ras_msg["caller_id"]):
                    return
            raise LoginException(errorText("USER_LOGIN","LOGIN_FROM_THIS_CALLER_ID_DENIED"))
        elif not self.allow_no_caller_id:
             raise LoginException(errorText("USER_LOGIN","LOGIN_FROM_THIS_CALLER_ID_DENIED"))
        
    def _reload(self):
        user_plugin.AttrCheckUserPlugin._reload(self)
        self.__initValues()

        
        
class LimitCallerIDAttrUpdater(AttrUpdater):

    def changeInit(self,caller_ids,allow_not_defined):
        caller_id_list=map(lambda caller_id:caller_id.strip(),MultiStr(caller_ids))

        for caller_id in caller_id_list:
            try:
                re.compile(caller_id)
            except:
                raise GeneralException(errorText("GENERAL","INVALID_CALLER_ID_PATTERN")%caller_id)

        toLog("%s,%s"%(caller_ids,allow_not_defined),LOG_DEBUG)
        
        self.useGenerateQuery({"limit_caller_id":",".join(caller_id_list),
                               "limit_caller_id_allow_not_defined":("1","0")[allow_not_defined==False]
                               })

    def deleteInit(self):
        self.useGenerateQuery(["limit_caller_id","limit_caller_id_allow_not_defined"])


class LimitCallerIDAttrSearcher(AttrSearcher):
    def run(self):
        search_helper=self.getSearchHelper()
        user_attrs=search_helper.getTable("user_attrs")
        user_attrs.likeStrSearch(search_helper,"limit_caller_id","limit_caller_id_op","limit_caller_id",MultiStr)


class LimitCallerIDAttrHandler(attribute.AttributeHandler):
    def __init__(self):
        attribute.AttributeHandler.__init__(self,attr_handler_name)
        self.registerAttrUpdaterClass(LimitCallerIDAttrUpdater,["limit_caller_id","limit_caller_id_allow_not_defined"])
        self.registerAttrSearcherClass(LimitCallerIDAttrSearcher)

