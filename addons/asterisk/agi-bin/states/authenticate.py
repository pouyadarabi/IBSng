import xmlrpclib
import ibs_agi
from lib import request
from lib.error import *


def init():
    ibs_agi.getStateMachine().registerState("AUTHENTICATE",authenticate)

def authenticate(username,password):
    req=request.Request()
    try:
        if ibs_agi.getConfig().getValue("debug"):
            toLog("Authenticate: Username %s Password %s"%(username,password))

        credit=req.send("authenticate",True,username=username,password=password)
    except xmlrpclib.Fault,e:
        ibs_agi.getSelectedLanguage().sayError(e.faultString)
        credit=0

        if ibs_agi.getConfig().getValue("debug"):
            toLog("Authenticate: Error: %s"%e.faultString)

    else:
        ibs_agi.getConfig().setValue("authenticated",True)
        
        if ibs_agi.getConfig().getValue("debug"):
            toLog("Authenticate: Credit %s"%credit)

    return credit
