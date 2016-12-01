"""
    VoIP Preferred language, keep 2 letter language code
"""
from core.user import user_plugin,user_main,attribute
from core.user.attr_updater import AttrUpdater
from core.user.attr_searcher import AttrSearcher
from core.ibs_exceptions import *
from core.errors import errorText
from core.lib.general import *

def init():
    user_main.getAttributeManager().registerHandler(VoIPPreferredLanguageAttrHandler(),["voip_preferred_language"],["voip_preferred_language"],[])

class VoIPPreferredLanguageAttrUpdater(AttrUpdater):
    def changeInit(self,voip_preferred_language):
        self.useGenerateQuery({"voip_preferred_language":voip_preferred_language})

    def deleteInit(self):
        self.useGenerateQuery(["voip_preferred_language"])

class VoIPPreferredLanguageAttrSearcher(AttrSearcher):
    def run(self):
        search_helper=self.getSearchHelper()
        user_attrs=search_helper.getTable("user_attrs")
        user_attrs.likeStrSearch(search_helper,"voip_preferred_language","voip_preferred_language_op","voip_preferred_language")


class VoIPPreferredLanguageAttrHandler(attribute.AttributeHandler):
    def __init__(self):
        attribute.AttributeHandler.__init__(self,"voip_preferred_language")
        self.registerAttrUpdaterClass(VoIPPreferredLanguageAttrUpdater,["voip_preferred_language"])
        self.registerAttrSearcherClass(VoIPPreferredLanguageAttrSearcher)


