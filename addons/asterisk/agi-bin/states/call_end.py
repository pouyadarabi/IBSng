import xmlrpclib
import ibs_agi
from lib import request
from lib.error import *

def init():
    ibs_agi.getStateMachine().registerState("CALL_END",callEnd)

def callEnd(duration, status):
    """
    """
    req=request.Request()
    try:
        if ibs_agi.getConfig().getValue("debug"):
            toLog("CallEnd: duration %s status %s"%(duration,status))

        (duration,used_credit)=req.send("callEnd",True,duration=duration,dc_cause=status)

        if ibs_agi.getConfig().getValue("debug"):
            toLog("CallEnd: duration %s used_credit %s"%(duration,used_credit))

    except xmlrpclib.Fault,e:
        logException()
        duration=used_credit=0

    return duration,used_credit

