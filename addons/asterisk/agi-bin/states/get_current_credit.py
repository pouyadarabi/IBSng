import xmlrpclib
import ibs_agi
from lib import request
from lib.error import *

def init():
    ibs_agi.getStateMachine().registerState("GET_CURRENT_CREDIT",getCurrentCredit)

def getCurrentCredit():
    """
        get current credit of user
        raise an IBSException if error happens
    """
    req=request.Request()
    try:
        credit=req.send("getUserCredit",True)
    except xmlrpclib.Fault,e:
        logException()
        ibs_agi.getSelectedLanguage().sayPrompt("unknown_problem")
        raise IBSException(e.faultString)
    else:
        if ibs_agi.getConfig().getValue("debug"):
            toLog("getCurrentCredit: %s"%credit)
        
        return credit