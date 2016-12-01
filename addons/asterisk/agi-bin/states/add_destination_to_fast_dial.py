import xmlrpclib
import ibs_agi
from lib import request
from lib.error import *


def init():
    ibs_agi.getStateMachine().registerState("ADD_DESTINATION_TO_FAST_DIAL",addDestinationToFastDial)

def addDestinationToFastDial(_index, destination):
    """
        add "destination" to "_index" of fast dials of current user
    """
    _index=int(_index)

    if ibs_agi.getConfig().getValue("debug"):
        toLog("addDestinationToFastDial: Index: %s Destination: %s"%(_index,destination))

    req=request.Request()
    try:
        last_number=req.send("addDestinationToFastDial",True,index=_index,destination=destination)
    except xmlrpclib.Fault,e:
        logException()
        ibs_agi.getSelectedLanguage().sayPrompt("add_destination_to_fast_dial_failure")
        return 
    else:
        for f in [lambda:ibs_agi.getSelectedLanguage().sayPrompt("pre_add_destination_to_fast_dial_success"),
                  lambda:ibs_agi.getSelectedLanguage().sayDigits(destination),
                  lambda:ibs_agi.getSelectedLanguage().sayPrompt("mid_add_destination_to_dast_dial_success"),
                  lambda:ibs_agi.getSelectedLanguage().sayDigit(_index),
                  lambda:ibs_agi.getSelectedLanguage().sayPrompt("post_add_destination_to_dast_dial_success")]:
            digit=f()
            if digit:
                break
        
                
        


    