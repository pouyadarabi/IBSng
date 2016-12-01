from core.ibs_exceptions import *
from core.errors import errorText
from core.user import user_main

class UserServerAuth:
    def checkAuth(self,username,password,auth_type):
        """
            check user authentication, for server requests. return loaded_user of authenticated user
            username(string): username
            password(Password Instance):
            auth_type(string): requested authentication type. Can be either "NORMAL_USER" or "VOIP_USER"
        """
        if auth_type == "NORMAL_USER":
            loaded_user = user_main.getUserPool().getUserByNormalUsername(username)
            pass_attr_name = "normal_password"
            
        elif auth_type == "VOIP_USER":
            loaded_user = user_main.getUserPool().getUserByVoIPUsername(username)
            pass_attr_name = "voip_password"
        
        self.__checkUserPassword(loaded_user,pass_attr_name,password)

        return loaded_user
        
    def __checkUserPassword(self,loaded_user,attr_name,password):
        if not password == loaded_user.getUserAttrs()[attr_name]:
            raise GeneralException(errorText("USER_LOGIN","WRONG_PASSWORD"))

    