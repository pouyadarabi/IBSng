from core.user import user_main

class LoadedUser:
    """
        Loaded User instances are keep in memory and user pool
        Loaded User is a container of user information, and should be reloadable.
        All of information we contain maybe changed so implemention should consider this
    """
    def __init__(self, basic_user, user_attrs):
        """
            basic_user(BasicUser instance): basic user information
            user_attrs(UserAttributes instance): user attribute instance
        """
        self.__setInternalVars(basic_user, user_attrs)
        self.online_flag=False

    def __setInternalVars(self, basic_user, user_attrs):
        self.basic_user=basic_user
        self.user_attrs=user_attrs

    def getBasicUser(self):
        return self.basic_user
        
    def getUserAttrs(self):
        return self.user_attrs

    def getUserID(self):
        return self.getBasicUser().getUserID()

    def hasNormalLogin(self):
        return self.getUserAttrs().hasAttr("normal_username")
    
    def getNormalUsername(self):
        return self.getUserAttrs().getAttr("normal_username")
        
    def hasAttr(self, attr_name):
        return self.getUserAttrs().hasAttr(attr_name)

    def userHasAttr(self, attr_name):
        return self.getUserAttrs().userHasAttr(attr_name)

    def getUserInfo(self, date_type):
        """
            return a dic of user informations, useful for passing to interface
        """
        return {"basic_info":self.getBasicUser().getInfo(date_type), 
                "attrs":user_main.getAttributeManager().parseAttrs(self.getUserID(), 
                                                                   "user", 
                                                                   self.getUserAttrs().getAllAttrs(), 
                                                                   date_type), 
#               "raw_attrs":self.getUserAttrs().getAllAttrs(),
                "online_status":self.isOnline()
               }        
        
    def setOnlineFlag(self, new_status):
        self.online_flag=new_status

    def isOnline(self):
        return self.online_flag

    def _reload(self, new_loaded_user):
        self.__setInternalVars(new_loaded_user.basic_user, new_loaded_user.user_attrs)

