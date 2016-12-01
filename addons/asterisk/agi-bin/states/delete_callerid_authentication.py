import xmlrpclib
import ibs_agi
from lib import request
from lib.error import *

def init():
    ibs_agi.getStateMachine().registerState("DELETE_CALLERID_AUTHENTICATION",deleteCallerIDAuthentication)

def deleteCallerIDAuthentication():
    """
        delete Caller ID Authentication from current user caller ids
    """
    req=request.Request()
    try:
        last_number=req.send("deleteCallerIDAuthentication",True)
    except xmlrpclib.Fault,e:
        if e.faultString=="CALLER_ID_NOT_EXISTS":
            ibs_agi.getSelectedLanguage().sayPrompt("delete_callerid_authentication_not_exists")
        else:
            logException()
            ibs_agi.getSelectedLanguage().sayPrompt("delete_callerid_authentication_failure")
        
        return 
    else:
        ibs_agi.getSelectedLanguage().sayPrompt("delete_callerid_authentication_success")
        
