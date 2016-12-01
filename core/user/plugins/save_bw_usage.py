from core.user import user_plugin,user_main,attribute
from core.user.attr_updater import AttrUpdater
from core.user.attr_searcher import AttrSearcher
from core.ibs_exceptions import *
from core.errors import errorText
from core.lib.general import *

def init():
    user_main.getAttributeManager().registerHandler(SaveBWUsageAttrHandler(),["save_bw_usage"],["save_bw_usage"],[])

        
class SaveBWUsageAttrUpdater(AttrUpdater):
    def changeInit(self):
        self.useGenerateQuery({"save_bw_usage":""})

    def deleteInit(self):
        self.useGenerateQuery(["save_bw_usage"])

class SaveBWUsageAttrSearcher(AttrSearcher):
    def run(self):
        search_helper=self.getSearchHelper()
        user_attrs=search_helper.getTable("user_attrs")
        user_attrs.hasAttrSearch(search_helper,"save_bw_usage","save_bw_usage")

class SaveBWUsageAttrHandler(attribute.AttributeHandler):
    def __init__(self):
        attribute.AttributeHandler.__init__(self,"save_bw_usage")
        self.registerAttrUpdaterClass(SaveBWUsageAttrUpdater,[])
        self.registerAttrSearcherClass(SaveBWUsageAttrSearcher)
