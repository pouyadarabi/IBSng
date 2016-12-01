class Handler: #ABSTRACT
    """
        this is parent class for all handlers
        all handlers must set their name, and register their fucntions using register method
        so it'll return it's own name and methods . Hanlder methods can be called
        by "name"."method"("args") syntax.
        HandlerManagers use handler instances and call their methods on demand. As IBS uses threads
        for multiple requests, handlers must take care of multi threading issues if necassary.
        It's better not to use global/object variables for changing and use local variables instead
    """
    def __init__(self,handler_name):
        self.__handler_name=handler_name
        self.__handler_methods=[]
     
    def getHandlerName(self):
        """
            return name of handler that will be used in xmlrpc calls
        """
        return self.__handler_name
        
    def getHandlerMethods(self):
        """
            return a list of name strings that represent this handler methods
            this list is used to see if this handler has such method, and method is callable
            via rpc requests
        """
        return self.__handler_methods


    def registerHandlerMethod(self,method_name):
        """
            register a new method into this handler
        """
        if method_name in self.__handler_methods:
            raise HandlerException("Duplicate registration of method %s"%method_name)
        self.__handler_methods.append(method_name)
