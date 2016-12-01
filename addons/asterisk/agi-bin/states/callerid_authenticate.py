import xmlrpclib
import ibs_agi
from lib import request
from lib.error import *

def init():
    ibs_agi.getStateMachine().registerState("CALLERID_AUTHENTICATE",callerIDAuthenticate)

def callerIDAuthenticate():
    if ibs_agi.getConfig().getValue("debug"):
        toLog("CallerIDAuthenticate: caller_id: %s"%ibs_agi.getConfig().getValue("caller_id"))
        
    req=request.Request()
    try:
        (username,credit,language)=req.send("preAuthenticate",True)
    except xmlrpclib.Fault:
        credit=0
    else:
        ibs_agi.getConfig().setValue("authenticated",True)
        ibs_agi.getConfig().setValue("pre_authenticated",True)
        ibs_agi.getConfig().setValue("username",username)
        if ibs_agi.getLangManager().getLanguage(language)!=None: #language offered?
            ibs_agi.getConfig().setValue("language",language)

        if ibs_agi.getConfig().getValue("debug"):
            toLog("CallerIDAuthenticate: username:%s credit:%s language:%s"%(username,credit,language))

        
    return credit
