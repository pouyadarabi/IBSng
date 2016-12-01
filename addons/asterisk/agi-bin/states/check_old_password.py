import xmlrpclib
import ibs_agi
from lib import request
from lib.error import *

def init():
    ibs_agi.getStateMachine().registerState("CHECK_OLD_PASSWORD",checkOldPassword)

def checkOldPassword(old_password):
    """
        check old password, return True if password was correct
        otherwise return False
    """
    req=request.Request()
    try:
        pass_correct=req.send("checkPassword",True,password=old_password)
    except xmlrpclib.Fault,e:
        logException()
        return 
    else:
        if not pass_correct:
            ibs_agi.getSelectedLanguage().sayPrompt("old_password_incorrect")   
    
        return pass_correct