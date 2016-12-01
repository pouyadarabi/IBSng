import telnetlib
import re

EOL="\r\n"

class AsteriskManager:
    response_pattern=re.compile("Response: (.+)\nActionID: (.+)\nMessage: (.+)",re.M)
    
    def __init__(self, host, port, username, secret, timeout):
        """
            host(str): ip address of asterisk server
            port(int): port of manager
            username(str): username to login in manager
            secret(str): asterisk manager secret
            timeout(str): connection timeout
        """
        self.host=host
        self.port=port
        self.username=username
        self.secret=secret
        self.timeout=timeout
        
        self.action_id=0L

    def run(self, action, dic_args):
        """
            establis a connection and do action with dic_args
            return message return by manager if command run successfully, 
            else raise an exception

            action(str): action string eg. hangup
            dic_args(dic of str): dictionry containing other arguments eg. {channel:sip/123}
        """
        connection=self.__connect()
        try:
            self.__login(connection)
            return self.__runCommand(connection, action, dic_args)
        finally:
            self.__destroy(connection)
    
    def __login(self, connection):
        """
            login to manager, raise an exception if login was unsuccessful
        """
        self.__runCommand(connection, "Login", {"Username":self.username, "Secret":self.secret})


    def __runCommand(self, connection, action, dic_args):
        response, action_id, message= self.__doCommand(connection, action, dic_args)
        
        if response.strip() == "Success":
            return message
        else:
            raise Exception(message)

    def __doCommand(self, connection, action, dic_args):
        """
            run command and return a tuple of (response, action_id, message)
        """
        dic_args["Action"]=action
        dic_args["ActionID"]=self.__getActionID()
        for name in dic_args:
            connection.write("%s: %s%s"%(name,dic_args[name],EOL))
        connection.write(EOL)
        _index, match_obj, text=connection.expect([self.response_pattern],self.timeout)
        if _index==-1:
            raise Exception("Timeout Occured")
        return match_obj.groups()
        
    def __getActionID(self):
        self.action_id+=1
        return self.action_id
        
    def __connect(self):
        return telnetlib.Telnet(self.host,self.port)

    def __destroy(self, connection):
        connection.close()
