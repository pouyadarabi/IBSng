from core.ibs_exceptions import *
from core.errors import errorText
from core.lib.general import *


def init():
    global handlers_manager
    handlers_manager=HandlersManager()
    
def getManager():
    return handlers_manager

class HandlersManager:
    def __init__(self):
        from core.server import request,response
        self.__handler_instances={}
        self.request=request
        self.response=response

    def handlerRegistered(self, name):
        """
            return True if handler with "name" is already registered
        """
        return name in self.__handler_instances


    def registerHandler(self,handler_obj):
        """
            register a new handler
            handler_obj:object of handler
        """
        name=handler_obj.getHandlerName()
        if self.handlerRegistered(name):
            raise HandlerException("Handler --%s-- already registered"%name)
        
        self.__handler_instances[name]=handler_obj

    def dispatch(self,method_name,params,client_address):
        """
            dispatch and run a request that came from xmlrpcserver
        """
        try:
            handler_name,method=self.__parseMethodName(method_name)
            handler_obj=self.__getHandlerObj(handler_name)
            self.__checkMethod(handler_obj,method)
            request_obj=self.__createRequestObj(handler_obj,method,params,client_address)
            self.__checkAuthentication(request_obj)
            ret_val=self.__run(request_obj)
            return self.__returnResponse(ret_val)
        except (GeneralException,LoginException,PermissionException),e:
            self.__returnError(e.__str__())
        except DBException,e:
            self.__returnError(e.__str__().split("\n")[0])
        except Exception,e:
            logException(LOG_ERROR,"dispatch")
            self.__returnError(e.__str__())
        except:
            logException(LOG_ERROR,"dispatch")
            self.__returnError(errorText("GENERAL","INTERNAL_ERROR"))
        

    def __checkMethod(self,handler_obj,method):
        """
            check if "handler_obj" has server callable method "method"
            raise a handlerException if it hasn't
        """
        if method not in handler_obj.getHandlerMethods():
            raise HandlerException("Handler --%s-- has not method --%s--"%(handler_obj.getHandlerName(),method))

    def __getHandlerObj(self,handler_name):
        """
            return handler object with name "handler_name"
            or raise a handlerException
        """
        try:
            return self.__handler_instances[handler_name]
        except KeyError:
            raise HandlerException("Handler --%s-- not found"%handler_name)

    def __parseMethodName(self,method_name):
        """
            parse method name and return handler_name,method
            method_names must be in format "handlername.method" else we'll
            raise an exception
        """
        sp=method_name.split(".",1)
        if len(sp)!=2:
            raise HandlerException("parseMethodName: invalid method_name --%s--"%method_name)
        return (sp[0],sp[1])

    def __createRequestObj(self,handler_obj,method,params,client_address):
        """
            create and return request object     
        """
        return self.request.Request(handler_obj,method,params,client_address)
        
    def __checkAuthentication(self,request_obj):
        """
            check request authentication
        """
        request_obj.authenticate()

    def __run(self,request_obj):
        """
            run request handler
            it must return a response object
        """
        return apply(getattr(request_obj.handler_obj,request_obj.method),[request_obj])

    def __returnError(self,error_text):
        """
            return an error to server
        """
        raise XMLRPCFault(error_text)

    def __returnResponse(self,handler_ret_val):
    
        """
            return response from "handler_ret_val" to server
        """
        if isinstance(handler_ret_val,self.response.Response):
            return self.__returnResponseObj(handler_ret_val)
        elif handler_ret_val==None: #xmlrpc can't handler None values
            return ""
        else:
            return handler_ret_val
    
    def __returnResponseObj(self,response_obj):
        """
            return response of a handler, that returned a response_obj
        """
        if response_obj.hasError():
            return self.__returnError(response_obj.getError())
        else:
            return response_obj.getResponse()
