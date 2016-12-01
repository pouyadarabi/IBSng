from core.server import handler
from core.admin import admin_main
from core.lib.password_lib import Password
from core.user import user_main
from core.ibs_exceptions import *
from core.errors import errorText

class LoginHandler(handler.Handler):
    def __init__(self):
        handler.Handler.__init__(self,"login")
        self.registerHandlerMethod("login")
    
    def login(self,request):
        request.checkArgs("login_auth_name","login_auth_type","login_auth_pass")
        if request["login_auth_type"]==request.ADMIN:
            admin_main.getLoader().getAdminByName(request["login_auth_name"]).checkAuth(Password(request["login_auth_pass"]),\
                                      request.getRemoteAddr())

        elif request["login_auth_type"]==request.NORMAL_USER:
            user_main.getServerAuth().checkAuth(request["login_auth_name"],Password(request["login_auth_pass"]),request["login_auth_type"])
            
        elif request["login_auth_type"]==request.VOIP_USER:
            user_main.getServerAuth().checkAuth(request["login_auth_name"],Password(request["login_auth_pass"]),request["login_auth_type"])
            
        elif request["login_auth_type"]==request.MAIL:
            pass

        elif request["login_auth_type"]==request.ANONYMOUS:
            pass

        else:
            raise GeneralException(errorText("GENERAL","ACCESS_DENIED"))

        return True
                