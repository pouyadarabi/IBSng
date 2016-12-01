import xmlrpclib
import ibs_agi
from lib import request
from lib.error import *

def init():
    ibs_agi.getStateMachine().registerState("AUTHORIZE",authorize)

def authorize(destination):
    """
        check authorization of user for calling destination
        return number of seconds remaining or -1 for unlimited
        set config authorized variable if successfully authorized
    """
    req=request.Request()
    try:
        if ibs_agi.getConfig().getValue("debug"):
            toLog("Authorize: Destination %s"%destination)

        remaining_time=req.send("authorize",True,destination=destination)

    except xmlrpclib.Fault,e:
        ibs_agi.getSelectedLanguage().sayError(e.faultString)
        remaining_time=-1

        if ibs_agi.getConfig().getValue("debug"):
            toLog("Aurhorize: Error: %s"%e.faultString)

    else:
        ibs_agi.getConfig().setValue("authorized",True)

        if ibs_agi.getConfig().getValue("debug"):
            toLog("Aurhorize: RemainingTime: %s"%remaining_time)

        
    return remaining_time
