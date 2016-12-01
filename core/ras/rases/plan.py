from core.script_launcher import launcher_main
from core.ras.ras import GeneralUpdateRas
from core.ras import ras_main
from core import defs
from core.ibs_exceptions import *
from core.ras.msgs import RasMsg
from core.event import periodic_events
from core.user import user_main
from core import main
import threading,time

def init():
    ras_main.getFactory().register(PersistentLanRas,"Persistent Lan")

class PersistentLanRas(GeneralUpdateRas):
    type_attrs={"plan_kill":"%splan/kill"%defs.IBS_ADDONS,"plan_login":"%splan/login"%defs.IBS_ADDONS,"plan_inout_usage":"%splan/inout_usage"%defs.IBS_ADDONS,"plan_login_retry_interval":15}

    def init(self):

        self.onlines={}#mac_ip:{mac:mac,ip:ip,user_id:user_id}
        self.inouts={}#mac_ip:{"in_bytes":i,"out_bytes":o,"in_rate":,"out_rate":}
        self.waitings={}#user_id:ras_msg
        self.waiting_lock=threading.Lock()
        if main.isStarting():
            main.registerPostInitMethod(self.__postInitMethod)
        else:
            self.__postInitMethod()

        self.handle_reload=True
        self.last_onlines_update = 0

    def __postInitMethod(self):
        self.__addAllToWaitings()
        self.tryAllWaitings()
        self.__initLoginRetry()

####################################
    def tryAllWaitings(self):
        """
            try all entries in waiting list. Waitings are users whom didn't login successfully yet
        """
        self.waiting_lock.acquire()
        try:
            for user_id in self.waitings.keys():
                self.__tryUser(user_id)
        finally:
            self.waiting_lock.release()
        
    def __tryUser(self,user_id):
        success=self.__sendAuthenticateMsg(user_id)
        if success:
            self.__addToOnlines(self.waitings[user_id])
            self.__loginUser(self.waitings[user_id])
            del(self.waitings[user_id])
        
        
    def __sendAuthenticateMsg(self,user_id):
        ras_msg=self.waitings[user_id]
        return ras_msg.send()

    def __sendStopMsg(self,user_id,mac,ip):
        ras_msg=self.__createRasMsg("PERSISTENT_LAN_STOP",user_id,mac,ip)
        return ras_msg.send()

    def __createRasMsg(self,action,user_id,mac,ip):
        ras_msg=RasMsg(None,None,self)
        ras_msg["user_id"],ras_msg["mac"],ras_msg["remote_ip"]=user_id,mac,ip
        ras_msg["mac_ip"]="%s_%s"%(mac,ip)
        ras_msg["unique_id"]="mac_ip"
        ras_msg["persistent_lan"]=True
        ras_msg["start_accounting"]=True
        ras_msg["ip_assignment"]=False
        ras_msg.setAction(action)
        return ras_msg

###################################
    def __addToOnlines(self,ras_msg):
        self.onlines[ras_msg["mac_ip"]]={"ip":ras_msg["remote_ip"],"user_id":ras_msg["user_id"],"mac":ras_msg["mac"]}

    def __delFromOnlines(self,mac_ip):
        del(self.onlines[mac_ip])

###################################
    def __addAllToWaitings(self):
        """
            ask for users who use this ras as persistent lan, and add em to waiting list
        """     
        users=user_main.getActionManager().getPersistentLanUsers(self.getRasID())
        for user_dic in users:
            self.__addToWaitings(user_dic["user_id"],user_dic["persistent_lan_mac"].upper(),user_dic["persistent_lan_ip"])

    def __addToWaitings(self,user_id,mac,ip):
        self.waitings[user_id]=self.__createRasMsg("PERSISTENT_LAN_AUTHENTICATE",user_id,mac,ip)

    def __removeFromWaitings(self,user_id):
        del(self.waitings[user_id])

###################################
    def __loginUser(self,ras_msg):
        """
            called after a user successfully logged in by user part
        """
        return launcher_main.getLauncher().system(self.getAttribute("plan_login"),
                                                    [self.getRasIP(),ras_msg["mac"],ras_msg["remote_ip"]])
####################################
    def killUser(self,user_msg):
        """
            kill user, this will call "kill_port_command" attribute, 
            with user ppp interface numbers as argument
        """
        try:
            mac_ip=user_msg["mac_ip"].upper()
            try:
                user_dic=self.onlines[mac_ip]
            except KeyError:
                self.toLog("User %s with mac_ip %s wasn't online"%(user_msg["user_id"],user_msg["mac_ip"]))
                return 
                                
            ret=launcher_main.getLauncher().system(self.getAttribute("plan_kill"),
                                                       [self.getRasIP(),user_dic["mac"],user_dic["ip"]])
            self.__addToWaitings(user_dic["user_id"],user_dic["mac"],user_dic["ip"])
            self.__delFromOnlines(mac_ip)
            self.__sendStopMsg(user_dic["user_id"],user_dic["mac"],user_dic["ip"])
        except:
            logException(LOG_ERROR)

####################################
    def getUsage(self):
        """
            return a dic of onlines users in format {mac:{in_bytes":in_bytes,"out_bytes":out_bytes}}

            this will call "inout_usage" attribute, and read its output.
            output of the command should be in format:

            mac_ip in_bytes out_bytes
        """
        lines=self.__getInOutFromCLI()
        return self.__parseCLIInOut(lines)
    
    def __getInOutFromCLI(self):
        fd=launcher_main.getLauncher().popen(self.getAttribute("plan_inout_usage"),[self.getRasIP()])
        out_lines=fd.readlines()
        fd.close()
        return out_lines
        
    def __parseCLIInOut(self,lines):
        try:
            inout={}
            for line in lines:
                sp=line.strip().split()
                if len(sp)!=3:
                    toLog("Plan getOnlines: Can't parse line %s"%line,LOG_ERROR)
                    continue
                inout[sp[0]]={"in_bytes":long(sp[1]),"out_bytes":long(sp[2])}
        except:
            logException(LOG_ERROR)
        return inout

####################################    
    def updateInOutBytes(self):
        inouts=self.getUsage()
        inouts=self._calcRates(self.inouts, inouts)
        self.inouts=inouts

####################################
    def isOnline(self,user_msg):
        return self.onlines.has_key(user_msg["mac_ip"])
####################################
    def getInOutBytes(self, user_msg):
        try:
            mac_ip=user_msg["mac_ip"].upper()
            if mac_ip in self.inouts:
                return (self.inouts[mac_ip]["in_bytes"],self.inouts[mac_ip]["out_bytes"],self.inouts[mac_ip]["in_rate"],self.inouts[mac_ip]["out_rate"])
            else:
                return (0,0,0,0)
        except:
            logException(LOG_ERROR)
            return (-1,-1,-1,-1)
####################################
    def dispatch(self,user_msg):
        action=user_msg.getAction()
        if action=="PLAN_LOGIN_NEW_USER":
            return self.__planLoginUser(user_msg)
        elif action=="PLAN_REMOVE_USER":
            return self.__planRemoveUser(user_msg)
        else:
            self._raiseUnknownActionException(user_msg)     
        
    def __planLoginUser(self,user_msg):
        self.waiting_lock.acquire()
        try:
            self.__addToWaitings(user_msg["user_id"],user_msg["mac"],user_msg["ip"])
            self.__tryUser(user_msg["user_id"])
        finally:
            self.waiting_lock.release()

    def __planRemoveUser(self,user_msg):
        """
            user_msg should contain both mac and user_id
        """
        self.waiting_lock.acquire()
        try:
            self.killUser(user_msg)
            self.__removeFromWaitings(user_msg["user_id"])
        finally:
            self.waiting_lock.release()

#######################################
    def __initLoginRetry(self):
        self.plan_login_retry=PLanLoginRetry(self)
        periodic_events.getManager().register(self.plan_login_retry)

    def __removeLoginRetry(self):
        periodic_events.getManager().unRegister(self.plan_login_retry)

#########################################
    def unloaded(self):
        GeneralUpdateRas.unloaded(self)
        self.__removeLoginRetry()
##########################################
    def _reload(self):
        GeneralUpdateRas._reload(self)
        self.__removeLoginRetry()
        self.__initLoginRetry()

class PLanLoginRetry(periodic_events.PeriodicEvent):
    def __init__(self,ras_obj):
        self.ras_id=ras_obj.getRasID()
        periodic_events.PeriodicEvent.__init__(self,
                                               "plan ras %s login retry"%ras_obj.getRasIP(),
                                               int(ras_obj.getAttribute("plan_login_retry_interval"))*60,
                                               [],0)

    def run(self):
        ras_main.getLoader().getRasByID(self.ras_id).tryAllWaitings()

