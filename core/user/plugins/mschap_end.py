"""
    this module runs as the last plugin for login method and set mppe-keys and MS_CHAP2-Success attributes
    These are here, because we should ensure that we send them in an AccessAccept Packet
"""
from core.user import user_plugin,user_main,attribute
from core.errors import *
from core.ibs_exceptions import *

def init():
    user_main.getUserPluginManager().register("mschap_end",MSChapEndPlugin,9)
    
class MSChapEndPlugin(user_plugin.UserPlugin):
    def __init__(self,user_obj):
        user_plugin.UserPlugin.__init__(self,user_obj)
 
    def login(self,ras_msg):
        if ras_msg.hasAttr("ms_chap_response"):
            ras_msg.getReplyPacket().addMSChapMPPEkeys(self.user_obj.getUserAttrs()["normal_password"])

        elif ras_msg.hasAttr("ms_chap2_response"):
                authenticator_response=ras_msg.getRequestPacket().generateMSChap2AuthenticatorResponse( \
											  self.user_obj.getUserAttrs()["normal_username"],
                                                                                          self.user_obj.getUserAttrs()["normal_password"])

                ras_msg.getReplyPacket()["MS-CHAP2-Success"]=authenticator_response
                ras_msg.getReplyPacket().addMSChap2MPPEkeys(self.user_obj.getUserAttrs()["normal_password"],
                                                            ras_msg.getRequestPacket()["MS-CHAP2-Response"][0][26:]
                                                            )


