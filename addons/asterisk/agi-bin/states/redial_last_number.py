import xmlrpclib
import ibs_agi
from lib import request
from lib.error import *

def init():
    ibs_agi.getStateMachine().registerState("REDIAL_LAST_NUMBER",redialLastNumber)

def redialLastNumber():
    """
        get last number dialed by user and dial it
    """
    req=request.Request()
    try:
        last_number=req.send("getLastDestination",True)
    except xmlrpclib.Fault,e:
        logException()
        ibs_agi.getSelectedLanguage().sayPrompt("unknown_problem")
        return 
    else:
        if ibs_agi.getConfig().getValue("debug"):
            toLog("getLastDestination: %s"%last_number)
        
        if not last_number:
            ibs_agi.getSelectedLanguage().sayPrompt("destination_incorrect")
            return 
            
        return ibs_agi.getStateMachine().gotoState("DIAL",last_number)