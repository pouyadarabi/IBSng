from core.user import user_plugin,user_main,attribute
from core.errors import *
from core.ibs_exceptions import *
from core.lib.password_lib import Password

def init():
    user_main.getUserPluginManager().register("password",PasswordUserPlugin,1)
    
class PasswordUserPlugin(user_plugin.UserPlugin):
    def __init__(self,user_obj):
        user_plugin.UserPlugin.__init__(self,user_obj)
 
    def login(self,ras_msg):
        if ras_msg.hasAttr("pap_password"):
            if not ras_msg.getRequestPacket().PwDecrypt(ras_msg["pap_password"])==Password(self.user_obj.getUserAttrs()["normal_password"]):
                self.__raiseIncorrectPassword(ras_msg["pap_password"])

        elif ras_msg.hasAttr("chap_password"):
            if not ras_msg.getRequestPacket().checkChapPassword(self.user_obj.getUserAttrs()["normal_password"]):
                self.__raiseIncorrectPassword()

        elif ras_msg.hasAttr("ms_chap_response"):
            if not ras_msg.getRequestPacket().checkMSChapPassword(self.user_obj.getUserAttrs()["normal_password"]):
                self.__raiseIncorrectPassword()

        elif ras_msg.hasAttr("ms_chap2_response"):
            if not ras_msg.getRequestPacket().checkMSChap2Password(self.user_obj.getUserAttrs()["normal_username"],\
                                                                   self.user_obj.getUserAttrs()["normal_password"]):
                self.__raiseIncorrectPassword()

        elif ras_msg.hasAttr("voip_password"):
            if not ras_msg["voip_password"]==Password(self.user_obj.getUserAttrs()["voip_password"]):
                self.__raiseIncorrectPassword(ras_msg["voip_password"])

        elif ras_msg.hasAttr("voip_chap_password"):
            if not ras_msg.getRequestPacket().checkChapPassword(self.user_obj.getUserAttrs()["voip_password"]):
                self.__raiseIncorrectPassword()

        elif ras_msg.hasAttr("voip_digest_response"):
            if not ras_msg.getRequestPacket().checkDigestPassword(self.user_obj.getUserAttrs()["voip_password"]):
                self.__raiseIncorrectPassword()

#       else:
#           toLog("Unknown Password checking method",LOG_DEBUG)
#           self.__raiseIncorrectPassword()

    def __raiseIncorrectPassword(self, password=""):
        if password and password.isalnum():
            err_text = "%s %s"%(errorText("USER_LOGIN","WRONG_PASSWORD"), password)
        else:
            err_text = errorText("USER_LOGIN","WRONG_PASSWORD")

        raise LoginException(err_text)
