import ibs_agi
import xmlrpclib

class IBSRequest:
    def __init__(self, auth_name, auth_pass, auth_type):
        self.auth_name=auth_name
        self.auth_pass=auth_pass
        self.auth_type=auth_type

    def send(self, method_name, **kargs):
        server=xmlrpclib.ServerProxy("http://%s:%s"%ibs_agi.getConfig().getValue("IBSng_server"))
        kargs["auth_type"]=self.auth_type
        kargs["auth_name"]=self.auth_name
        kargs["auth_pass"]=self.auth_pass
        
        return getattr(server,method_name)(kargs)

class Request(IBSRequest):
    def __init__(self, asterisk_password=None):
        IBSRequest.__init__(self,"ANONYMOUS","ANONYMOUS","ANONYMOUS")
        if asterisk_password==None:
            asterisk_password=ibs_agi.getConfig().getValue("asterisk_password")
        
        self.asterisk_password=asterisk_password
        self.add_session_variables=False

    def send(self, method_name,add_session_variables=False,**kargs):
        """
            call method name with dictionary arguments and return the results
        """
        kargs["asterisk_password"]=ibs_agi.getConfig().getValue("asterisk_password")

        if add_session_variables:
            kargs["username"]=ibs_agi.getConfig().getValue("username")
            kargs["caller_id"]=ibs_agi.getConfig().getValue("caller_id")
            kargs["channel"]=ibs_agi.getConfig().getValue("channel")
            kargs["unique_id"]=ibs_agi.getConfig().getValue("unique_id")

        return apply(IBSRequest.send,[self,"asterisk.%s"%method_name],kargs)