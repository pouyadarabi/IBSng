"""
    This plugin take care of "try_single_session_h323" ras_msg attribute
"""
from core.user import user_plugin,user_main,attribute
from core.ibs_exceptions import *
from core.errors import errorText
from core.lib.general import *

DEBUG=False

def init():
    user_main.getUserPluginManager().register("h323_plugin",H323UserPlugin,1)

class H323UserPlugin(user_plugin.UserPlugin): 
    def login(self,ras_msg):
        if self.user_obj.getUserAttrs().hasAttr("multi_login"):
            multi_login=int(self.user_obj.getUserAttrs()["multi_login"])
        else:
            multi_login=1

        if DEBUG:
            toLog("h323UserPlugin: try: %s multi_login: %s"%(ras_msg.hasAttr("try_single_session_h323"),multi_login),LOG_DEBUG)

        if ras_msg.hasAttr("try_single_session_h323") and multi_login==1:
            if DEBUG:
                toLog("h323UserPlugin: setting single_session_h323",LOG_DEBUG)
            ras_msg["single_session_h323"]=True
        
        
