from core.user import user_plugin,user_main

from core.ibs_exceptions import *
from core.errors import errorText


def init():
    user_main.getUserPluginManager().register("terminate_cause_plugin",TerminateCause)

class TerminateCause(user_plugin.UserPlugin): 
    def logout(self, instance, ras_msg):
        if ras_msg.hasAttr("terminate_cause"):
            self.user_obj.getInstanceInfo(instance)["attrs"]["terminate_cause"] = ras_msg["terminate_cause"]
        

        