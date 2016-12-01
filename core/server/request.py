from core.ibs_exceptions import *
from core.lib.general import *
from core.lib.password_lib import Password
from core.errors import errorText
from core.server.response import Response
import types
from core.admin import admin_main
from core.user import user_main


class Request:
    ADMIN="ADMIN"
    NORMAL_USER="NORMAL_USER"
    VOIP_USER="VOIP_USER"
    MAIL="MAIL"
    ANONYMOUS="ANONYMOUS"
    AUTH_TYPES=[ADMIN,NORMAL_USER,VOIP_USER,MAIL,ANONYMOUS]
    def __init__(self,handler_obj,method,params,client_address):
        """
            params: List of a dic [{param_name:param_value,...}]
        """
        
        self.handler_obj=handler_obj
        self.method=method
        self.authenticated=0
        self.client_address=client_address

        try:
            params=self.__processParams(params)
        except:
            logException(LOG_ERROR,"proccessParams")
            raise HandlerException("Invalid parameters")

    def __getitem__(self,key):
        return self.params[key]

    def has_key(self,key):
        return self.params.has_key(key)

    def authenticate(self):
        """
            authenticate user who send this request
        """
        if self.auth_type==self.ADMIN:
            self.__checkAdminAuth()
        elif self.auth_type==self.NORMAL_USER:
            self.__checkNormalUserAuth()
        elif self.auth_type==self.VOIP_USER:
            self.__checkVoipUserAuth()
        elif self.auth_type==self.MAIL:
            self.__checkMailAuth()
        elif self.auth_type==self.ANONYMOUS:
            self.__checkAnonymousAuth()

        else:
            raise LoginException(errorText("GENERAL","INVALID_AUTH_TYPE"))
            
        self.authenticated=1


    def getResponse(self):
        """
            return a response obj
        """
        return Response()

    def getErrorResponse(self,error_text):
        """
            return a response obj with error flag set and error text as "error_text"
        """
        response_obj=Response()
        response_obj.setError(error_text)
        return response_obj
        
    
    def checkArgs(self,*args):
        """
            check if *args variables are passed via request.
            args should be strings, arguments that the handler excepts to be exists
        """
        for arg in args:
            if not self.params.has_key(arg):
                self.raiseIncompleteRequest(arg)

    def raiseIncompleteRequest(self,missing_arg):
        raise HandlerException(errorText("GENERAL","INCOMPLETE_REQUEST")%missing_arg)

    def raiseAccessDenied(self):
        raise HandlerException(errorText("GENERAL","ACCESS_DENIED"))
    
    def needAuthType(self,*args):
        """
            handler checks user that call the handler must have auth_type in "args" by calling
            this method
            ex. needAuthType("admin")
        """
        if self.auth_type not in args:
            self.raiseAccessDenied()    
    
    def hasAuthType(self,auth_type):
        """
            check if this request has auth type of "auth_type"
            for checking access to a handler use needAuthType
            this method is for multiple authtype handlers that want to check which authtype
            request has
        """
        if auth_type not in self.AUTH_TYPES:
            raise HandlerException(errorText("GENERAL","INVALID_AUTH_TYPE"))

        if self.auth_type == auth_type:
            return True
        else:
            return False

    def getRemoteAddr(self):
        """
            return client remote ip address
        """
        if self.client_address[0] in defs.TRUSTED_CLIENTS and self.params.has_key("auth_remoteaddr"):
            remote_addr=self.params["auth_remoteaddr"]
        else:
            remote_addr=self.client_address[0]

        return remote_addr

    def getAuthNameObj(self):
        """
            return object of auth_name, it's available for auth_types: admin 
            and not available for: anonymous
            if it's not available , an exception is raised
        """
        return self.auth_name_obj

    def __processParams(self,params):
        """
            process parameters, and delete special params like auth_type and auth_name
        """
        self.params=params[0]
        self.__processAuthParams()
        
        
    def __processAuthParams(self):
        """    
            check for auth_type auth_name and auth_pass in params
        """
        self.auth_name=self.params["auth_name"]
        self.auth_pass=Password(self.params["auth_pass"])
        self.auth_type=self.params["auth_type"]
        del(self.params["auth_name"],self.params["auth_pass"],self.params["auth_type"])

    def __checkAdminAuth(self):
        """
            check authentication for admins
        """
        admin_obj=admin_main.getLoader().getAdminByName(self.auth_name)
        admin_obj.checkServerAuth(self.auth_pass,self.getRemoteAddr())
        self.auth_name_obj=admin_obj
    
    def __checkNormalUserAuth(self):
        self.auth_name_obj=user_main.getServerAuth().checkAuth(self.auth_name,self.auth_pass,self.auth_type)

    def __checkVoipUserAuth(self):
        self.auth_name_obj=user_main.getServerAuth().checkAuth(self.auth_name,self.auth_pass,self.auth_type)

    def __checkMailAuth(self):
        pass
    
    def __checkAnonymousAuth(self):
        pass

    def getDateType(self):
        """
            each request can have a "date_type" in arguments that shows results date should be in that format
            if no date_type passed, gregorian dates are used
            values can be "gregorian" and "jalali"
        """
        if self.has_key("date_type") and self["date_type"] in ("gregorian","jalali","relative"):
            return self["date_type"]
        else:
            return "gregorian"

    def fixList(self,key):
        """
            some xmlrpc implementions return lists as dictionaries. 
            This method return value of key if it is a list, or convert it to list, if it's dictionary
        """
        if type(self[key])==types.DictType:
            return map(lambda x:self[key][`x`], xrange(len(self[key]))) #let's keep the order
            
        return key
