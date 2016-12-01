class Response:
    def __init__(self):
        self.error_flag=0
        self.error_text=None
        self.reponse=None
        
    def setError(self,error_text):
        """
            set error in this response
            this will set error flag, so xmlrpcserver will return a fault instead of real response
        """
        self.error_flag=1
        self.error_text=error_text
        
    def setResponse(self,response):
        """
            set response, when xmlrpcserver see this response obj, it will return
            response to client
        """
        self.response=response
    
    def hasError(self):
        """
            tell if this is an error response
        """
        return self.error_flag

    def getError(self):
        """
            return error text if it's set, caller must ensure the it's set
            by calling hasError
        """
        return self.error_text

    def getResponse(self):
        """
            return response
            note that caller must already check for error
        """
        return self.response