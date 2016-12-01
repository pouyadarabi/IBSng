from core.script_launcher import launcher_main
from core.ras.ras import GeneralUpdateRas
from core.ras import ras_main
from core import defs
from core.ibs_exceptions import *
import time

def init():
    ras_main.getFactory().register(PPPDRas, "pppd")

class PPPDRas(GeneralUpdateRas):
    type_attrs={"pppd_kill_port_command":"%spppd/kill"%defs.IBS_ADDONS, 
                "pppd_inouts_command":"%spppd/inouts"%defs.IBS_ADDONS, 
                "pppd_apply_bandwidth_limit":"%spppd/apply_bw_limit"%defs.IBS_ADDONS, 
                "pppd_remove_bandwidth_limit":"%spppd/remove_bw_limit"%defs.IBS_ADDONS, 
                "pppd_discover_mac_address":1, 
                "pppd_mac_script":"%spppd/get_mac"%defs.IBS_ADDONS, 
                "pppd_use_update_accounting":1, 
                "pppd_update_accounting_interval":1, 
                "pppd_reonline_users":0
                }

    def init(self):
        self.inouts = {}# dic in format port=>{"in_bytes":,"out_bytes":,"in_rate":,"out_rate":}
        self.onlines = {}# dic of port=>{"username":,"in_bytes":,"out_bytes": "last_update":}

####################################
    def killUser(self, user_msg):
        """
            kill user, this will call "kill_port_command" attribute, 
            with user ppp interface numbers as argument
        """
        self.__killUserOnPort(user_msg["port"])
        
    def __killUserOnPort(self, port):
        try:
            return launcher_main.getLauncher().system(self.getAttribute("pppd_kill_port_command"), [self.getRasIP(), port])
        except:
            logException(LOG_ERROR)

####################################
    def getInOuts(self):
        """
            return a dic of in/outs of  users in format {port_name:{"in_bytes":in_bytes,"out_bytes":out_bytes}}

            this will call "inouts_command" attribute, and read its output.
            output of the command should be in format:

            port_no in_bytes out_bytes
        """
        lines=self.__getInOutsFromCLI()
        return self.__parseCLIInOuts(lines)
    
    def __getInOutsFromCLI(self):
        fd=launcher_main.getLauncher().popen(self.getAttribute("pppd_inouts_command"), [self.getRasIP()])
        out_lines=fd.readlines()
        fd.close()
        return out_lines
        
    def __parseCLIInOuts(self, lines):
        try:
            inout_list={}
            for line in lines:
                sp=line.strip().split()
                if len(sp)!=3:
                    toLog("PPPd getInOuts: Can't parse line %s"%line, LOG_ERROR)
                    continue

                inout_list[sp[0]]={"in_bytes":long(sp[1]), "out_bytes":long(sp[2])}
        except:
            logException(LOG_ERROR)

        return inout_list

####################################    
    def updateInOutBytes(self):
        inouts=self.getInOuts()
        inouts=self._calcRates(self.inouts, inouts)
        self.inouts=inouts
####################################
    def isOnline(self, user_msg):
        if self.getAttribute("pppd_use_update_accounting"):
            return self.onlines.has_key(user_msg["port"]) and self.onlines[user_msg["port"]]["last_update"] >= \
                    time.time() - self.getAttribute("pppd_update_accounting_interval")*60
        else:
            return self.inouts.has_key(user_msg["port"])
####################################
    def getInOutBytes(self, user_msg):
        try:
            port=user_msg["port"]
            if port in self.inouts:
                return (self.inouts[port]["in_bytes"], self.inouts[port]["out_bytes"], self.inouts[port]["in_rate"], self.inouts[port]["out_rate"])
            elif port in self.onlines:
                return (self.onlines[port]["in_bytes"], self.onlines[port]["out_bytes"], 0, 0)
            else:
                return (0, 0, 0, 0)
        except:
            logException(LOG_ERROR)
            return (-1, -1, -1, -1)
####################################
    def __getClientMacAddress(self, station_ip):
        lines=self.__getClientMacAddressFromCLI(station_ip)
        if lines:
            return lines[0].strip()
        return ""

    def __getClientMacAddressFromCLI(self, station_ip):
        fd=launcher_main.getLauncher().popen(self.getAttribute("pppd_mac_script"), [self.getRasIP(), station_ip])
        out_lines=fd.readlines()
        fd.close()
        return out_lines
####################################
    def __addUniqueIdToRasMsg(self, ras_msg):
        ras_msg["unique_id"]="port"
        ras_msg["port"]=str(ras_msg.getRequestPacket()["NAS-Port"][0])

    def handleRadAuthPacket(self, ras_msg):
        self.__addUniqueIdToRasMsg(ras_msg)
        ras_msg.setInAttrs({"User-Name":"username"})
        ras_msg.setInAttrsIfExists({"User-Password":"pap_password", 
                                    "CHAP-Password":"chap_password", 
                                    "MS-CHAP-Response":"ms_chap_response", 
                                    "MS-CHAP2-Response":"ms_chap2_response", 
                                    "Calling-Station-Id":"station_ip"
                                    })

        if self.onlines.has_key(ras_msg["port"]):
                self.onlines[ras_msg["port"]]["in_bytes"], self.onlines[ras_msg["port"]]["out_bytes"]=0, 0

        if ras_msg.hasAttr("station_ip") and self.getAttribute("pppd_discover_mac_address"):
            ras_msg["mac"]=self.__getClientMacAddress(ras_msg["station_ip"])
            
        if self.getAttribute("pppd_use_update_accounting"):
            ras_msg.getReplyPacket()["Acct-Interim-Interval"] = self.getAttribute("pppd_update_accounting_interval")*60
        
        ras_msg.setAction("INTERNET_AUTHENTICATE")

####################################
    def handleRadAcctPacket(self, ras_msg):
        status_type=ras_msg.getRequestAttr("Acct-Status-Type")[0]
        self.__addUniqueIdToRasMsg(ras_msg)
        if status_type=="Start":

            ras_msg.setInAttrs({"User-Name":"username", "Framed-IP-Address":"remote_ip", "Acct-Session-Id":"session_id"})
            ras_msg["start_accounting"]=True
            ras_msg["update_attrs"]=["remote_ip", "start_accounting"]

            self.__addInOnlines(ras_msg)

            ras_msg.setAction("INTERNET_UPDATE")
        elif status_type=="Stop":

            ras_msg.setInAttrs({"User-Name":"username", 
                                "Framed-IP-Address":"remote_ip", 
                                "Acct-Session-Id":"session_id", 
                                "Acct-Output-Octets":"in_bytes", 
                                "Acct-Input-Octets":"out_bytes"})

            ras_msg.setInAttrsIfExists({"Acct-Terminate-Cause":"terminate_cause"})
                                
            try:
                self.inouts[ras_msg["port"]]["in_bytes"], self.inouts[ras_msg["port"]]["out_bytes"]=ras_msg["in_bytes"], ras_msg["out_bytes"]
            except KeyError:
                logException(LOG_DEBUG)
                
            ras_msg.setAction("INTERNET_STOP")

        elif status_type == "Alive":
            if not self.isUserOnline(ras_msg) and int(self.getAttribute("pppd_reonline_users")):
                self.tryToReOnline(ras_msg)
            else:
                self.__updateInOnlines(ras_msg)

        else:
            self.toLog("handleRadAcctPacket: invalid status_type %s"%status_type, LOG_ERROR)


#######################################
    def populateReOnlineRasMsg(self, ras_msg):
        GeneralUpdateRas.populateReOnlineRasMsg(self, ras_msg)
        
        ras_msg.setInAttrsIfExists({"Calling-Station-Id":"station_ip"})

    def tryToReOnlineResult(self, ras_msg, auth_success):
        if auth_success: 
            self.__addInOnlines(ras_msg)
        else:
            #auth failed
            self.__killUserOnPort(ras_msg["port"])

##########################################
    
    def __addInOnlines(self, ras_msg):

        pkt = ras_msg.getRequestPacket()
        if pkt.has_key("Acct-Output-Octets"):
            start_in_bytes = pkt["Acct-Input-Octets"][0]
            start_out_bytes = pkt["Acct-Output-Octets"][0]
        else:
            start_in_bytes = 0
            start_out_bytes = 0

        self.onlines[ras_msg["port"]] = {"username":ras_msg["username"], 
                                         "in_bytes":0, 
                                         "out_bytes":0, 
                                         "start_in_bytes":start_in_bytes, 
                                         "start_out_bytes":start_out_bytes, 
                                         "last_update":time.time()}

    def __updateInOnlines(self, ras_msg):
        if ras_msg["port"] in self.onlines:
            self.onlines[ras_msg["port"]]["last_update"] = time.time()
            self.onlines[ras_msg["port"]]["in_bytes"] = ras_msg.getRequestAttr("Acct-Output-Octets")[0]
            self.onlines[ras_msg["port"]]["out_bytes"] = ras_msg.getRequestAttr("Acct-Input-Octets")[0]
        else:
            self.toLog("Update accounting called for %s,%s while he's NOT on my online list"%(ras_msg.getRequestAttr("User-Name")[0], ras_msg["port"]))
        

####################################
    def applySimpleBwLimit(self, user_msg):
        """
            run apply/remove limit script. Name of script is in "pppd_apply_bandwidth_limit" attribute.
            Parameters ras_ip port limit_rate_kbytes will be passed to script. If ras is on seperate machin,
            Admin can change the script to apply limit on another ras or change pppd_apply_bandwidth_limit attribute
            
            WARNING: return Success even if script fails
            WARNING: script should not sleep or wait, it should return immediately
        """
        if user_msg["action"]=="apply":
            try:
                return launcher_main.getLauncher().system(self.getAttribute("pppd_apply_bandwidth_limit"), 
                                                            [self.getRasIP(), user_msg["port"], user_msg["rate_kbytes"]])
            except:
                logException(LOG_ERROR)
                return False
                
        elif user_msg["action"]=="remove":
            try:
                return launcher_main.getLauncher().system(self.getAttribute("pppd_remove_bandwidth_limit"), 
                                                            [self.getRasIP(), user_msg["port"]])
            except:
                logException(LOG_ERROR)
                return False
                
        return True
        