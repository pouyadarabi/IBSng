from core.ras.ras import GeneralUpdateRas
from core.ras import ras_main
from core import defs
from core.ibs_exceptions import *
from core.script_launcher import launcher_main

def init():
    ras_main.getFactory().register(PortSlaveRas,"Portslave")

class PortSlaveRas(GeneralUpdateRas):
    type_attrs={"portslave_kill_port_command":"%sportslave/kill"%defs.IBS_ADDONS,
                "portslave_list_users_command":"%sportslave/list_users"%defs.IBS_ADDONS}

    def init(self):

        self.onlines = {}# dic of port=>{"username":,"in_bytes":,"out_bytes":}

####################################
    def killUser(self,user_msg):
        """
            kill user, this will call "kill_port_command" attribute, 
            with user port as argument
        """
        try:
            return launcher_main.getLauncher().system(self.getAttribute("portslave_kill_port_command"),
                                                        [self.getRasIP(),user_msg["port"]])
        except:
            logException(LOG_ERROR)

####################################
    def getOnlineUsers(self):
        """
            return a dic of in/outs of users in format {port_name:{"in_bytes":in_bytes,"out_bytes":out_bytes,"username":username}}

            this will call "list_users_command" attribute, and read its output.
            output of the command should be in format:

            port username in_bytes out_bytes

        """
        lines=self.__getOnlinesFromCLI()
        return self.__parseCLIOnlines(lines)
    
    def __getOnlinesFromCLI(self):
        fd=launcher_main.getLauncher().popen(self.getAttribute("portslave_list_users_command"),[self.getRasIP()])
        out_lines=fd.readlines()
        fd.close()
        return out_lines
        
    def __parseCLIOnlines(self,lines):
        try:
            users_list={}
            for line in lines:
                sp=line.strip().split()
                if len(sp)!=4:
                    self.toLog("Can't parse line %s"%line,LOG_ERROR)
                    continue

                users_list[sp[0]]={"username":sp[1],"in_bytes":long(sp[2]),"out_bytes":long(sp[3])}
        except:
            logException(LOG_ERROR)

        return users_list

####################################    
    def updateInOutBytes(self):
        onlines=self.getOnlineUsers()
        onlines=self._calcRates(self.onlines, onlines)
        self.onlines=onlines
####################################
    def isOnline(self,user_msg):
        return self.onlines.has_key(user_msg["port"])
####################################
    def getInOutBytes(self, user_msg):
        try:
            port=user_msg["port"]
            return (self.onlines[port]["in_bytes"],self.onlines[port]["out_bytes"],self.onlines[port]["in_rate"],self.onlines[port]["out_rate"])
        except KeyError:
            return (0,0,0,0)
####################################
    def __addUniqueIdToRasMsg(self,ras_msg):
        ras_msg["unique_id"]="port"
        ras_msg["port"]=str(ras_msg.getRequestPacket()["NAS-Port"][0])

    def handleRadAuthPacket(self,ras_msg):
        self.__addUniqueIdToRasMsg(ras_msg)
        ras_msg.setInAttrs({"User-Name":"username"})
        ras_msg.setInAttrsIfExists({"User-Password":"pap_password",
                                    "CHAP-Password":"chap_password",
                                    "MS-CHAP-Response":"ms_chap_response",
                                    "MS-CHAP2-Response":"ms_chap2_response",
                                    "Calling-Station-Id":"caller_id"
                                    })

        if self.onlines.has_key(ras_msg["port"]):
                self.onlines[ras_msg["port"]]["in_bytes"],self.onlines[ras_msg["port"]]["out_bytes"]=0,0

        ras_msg.setAction("INTERNET_AUTHENTICATE")

####################################
    def handleRadAcctPacket(self,ras_msg):
        status_type=ras_msg.getRequestAttr("Acct-Status-Type")[0]
        self.__addUniqueIdToRasMsg(ras_msg)
        if status_type=="Start":
            ras_msg.setInAttrs({"User-Name":"username","Framed-IP-Address":"remote_ip","Acct-Session-Id":"session_id"})
            ras_msg["start_accounting"]=True
            ras_msg["update_attrs"]=["remote_ip","start_accounting"]

            ras_msg.setAction("INTERNET_UPDATE")
        elif status_type=="Stop":
            ras_msg.setInAttrs({"User-Name":"username","Framed-IP-Address":"remote_ip","Acct-Session-Id":"session_id","Acct-Output-Octets":"in_bytes","Acct-Input-Octets":"out_bytes"})
            try:
                self.onlines[ras_msg["port"]]["in_bytes"],self.onlines[ras_msg["port"]]["out_bytes"]=ras_msg["in_bytes"],ras_msg["out_bytes"]
            except KeyError:
                #logException(LOG_DEBUG)
                pass

            ras_msg.setAction("INTERNET_STOP")
        else:
            self.toLog("handleRadAcctPacket: invalid status_type %s"%status_type,LOG_ERROR)
        
