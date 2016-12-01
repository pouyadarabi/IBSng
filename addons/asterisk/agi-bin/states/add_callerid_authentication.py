import xmlrpclib
import ibs_agi
from lib import request
from lib.error import *

def init():
    ibs_agi.getStateMachine().registerState("ADD_CALLERID_AUTHENTICATION",addCallerIDAuthentication)

def addCallerIDAuthentication():
    """
        Add Caller ID Authentication to current user caller ids
    """
    caller_id=ibs_agi.getConfig().getValue("caller_id")
    if not caller_id or caller_id=="unknown":
        ibs_agi.getSelectedLanguage().sayPrompt("invalid_callerid")
        return
    
    req=request.Request()
    try:
        last_number=req.send("addCallerIDAuthentication",True)
    except xmlrpclib.Fault,e:
        logException()
        ibs_agi.getSelectedLanguage().sayPrompt("add_callerid_authentication_failure")
        return 
    else:
        ibs_agi.getSelectedLanguage().sayPrompt("add_callerid_authentication_success")
        
