import xmlrpclib
import ibs_agi
from lib import request
from lib.error import *

def init():
    ibs_agi.getStateMachine().registerState("GET_FAST_DIAL_DESTINATION_FROM_IBS",getFastDialIndexFromIBS)

def getFastDialIndexFromIBS(_index):
    """
        get fast dial index destination from ibs
        may raise an IBSException
    """
    _index=int(_index)
    req=request.Request()
    try:
        destination=req.send("getFastDialDestination",True,index=_index)
    except xmlrpclib.Fault,e:
        logException()
        ibs_agi.getSelectedLanguage().sayPrompt("unknown_problem")
        raise IBSException(e.faultString)
    else:
        if ibs_agi.getConfig().getValue("debug"):
            toLog("getFastDialIndexFromIBS: %s"%destination)

        return destination
            
