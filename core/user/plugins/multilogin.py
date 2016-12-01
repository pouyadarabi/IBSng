from core.user import user_plugin,user_main,attribute
from core.user.attr_updater import AttrUpdater
from core.user.attr_searcher import AttrSearcher
from core.ibs_exceptions import *
from core.errors import errorText
from core.lib.general import *

attr_handler_name="multi login"
def init():
    user_main.getUserPluginManager().register("multi_login",MultiLogin)
    user_main.getAttributeManager().registerHandler(MultiLoginAttrHandler(),["multi_login"],["multi_login"],[])

class MultiLogin(user_plugin.UserPlugin): 
    def __init__(self,user_obj):
        user_plugin.UserPlugin.__init__(self,user_obj)
        self.__setMultiLogin()
        self.multilogin_allowed=[] #does instances allow multi login?

    def __setMultiLogin(self):
        self.multi_login=1
        if self.user_obj.getUserAttrs().hasAttr("multi_login"):
            self.multi_login=int(self.user_obj.getUserAttrs()["multi_login"])

    def login(self,ras_msg):
        if self.user_obj.instances>self.multi_login:
            raise LoginException(errorText("USER_LOGIN","MAX_CONCURRENT"))

        if ras_msg.hasAttr("multi_login"):
            self.multilogin_allowed.append(ras_msg["multi_login"])
        else:
            self.multilogin_allowed.append(True)
        
        if False in self.multilogin_allowed and self.user_obj.instances>1:
            raise LoginException(errorText("USER_LOGIN","RAS_DOESNT_ALLOW_MULTILOGIN"))

    def logout(self,instance,ras_msg):
        if len(self.multilogin_allowed)>=instance:
            del(self.multilogin_allowed[instance-1])

    def _reload(self):
        self.__setMultiLogin()
        
class MultiLoginAttrUpdater(AttrUpdater):
    def changeInit(self,multi_login):
        try:
            self.multi_login=int(multi_login)
        except ValueError:
            raise GeneralException(errorText("USER_ACTIONS","INVALID_MULTI_LOGIN"))

        if self.multi_login < 0 or self.multi_login > 255:
            raise GeneralException(errorText("USER_ACTIONS","INVALID_MULTI_LOGIN"))

        self.useGenerateQuery({"multi_login":self.multi_login})

    def deleteInit(self):
        self.useGenerateQuery(["multi_login"])  

class MultiLoginAttrSearcher(AttrSearcher):
    def run(self):
        self.ltgtSearchOnUserAndGroupAttrs("multi_login","multi_login_op","multi_login")

class MultiLoginAttrHandler(attribute.AttributeHandler):
    def __init__(self):
        attribute.AttributeHandler.__init__(self,attr_handler_name)
        self.registerAttrUpdaterClass(MultiLoginAttrUpdater,["multi_login"])
        self.registerAttrSearcherClass(MultiLoginAttrSearcher)
