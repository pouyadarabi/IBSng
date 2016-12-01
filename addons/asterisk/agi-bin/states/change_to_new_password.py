import xmlrpclib
import ibs_agi
from lib import request
from lib.error import *

def init():
    ibs_agi.getStateMachine().registerState("CHANGE_TO_NEW_PASSWORD",changeToNewPassword)

def changeToNewPassword(new_password):
    """
    """
    req=request.Request()
    try:
        req.send("changePassword",True,password=new_password)
    except xmlrpclib.Fault,e:
        ibs_agi.getSelectedLanguage().sayPrompt("change_password_failure")
        logException()
        return 
    else:
        ibs_agi.getSelectedLanguage().sayPrompt("change_password_success")      
    
