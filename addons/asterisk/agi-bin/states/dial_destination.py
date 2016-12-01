import ibs_agi
from lib.error import *

def init():
    ibs_agi.getStateMachine().registerState("DIAL_DESTINATION",dialDestination)

def dialDestination(destination, remaining_time):
    """
        dial destination and return duration of call
        if call was unsuccessful say the error
    """
    dial_str=ibs_agi.getConfig().getDialString(destination)
    if remaining_time>0:
        dial_str+="L(%s:30000)"%(int(remaining_time)*1000)
        ibs_agi.getAGI().set_variable("LIMIT_WARNING_FILE",ibs_agi.getSelectedLanguage()._getFilePath("disconnect_30"))
        ibs_agi.getAGI().set_variable("LIMIT_TIMEOUT_FILE",ibs_agi.getSelectedLanguage()._getFilePath("you_have_been_disconnected"))

    if ibs_agi.getConfig().getValue("debug"):
        toLog("Dial: Destination %s DialString %s"%(destination,dial_str))

    ibs_agi.getAGI().appexec("Dial",dial_str)
        
    duration=0
    status=ibs_agi.getAGI().get_variable("DIALSTATUS")
    

    if status in ["CHANUNAVAIL","CONGESTION"]:
        ibs_agi.getSelectedLanguage().sayPrompt("destination_out_of_service")
    elif status in ["BUSY"]:
        ibs_agi.getSelectedLanguage().sayPrompt("destination_busy")
    elif status in ["NOANSWER"]:
        ibs_agi.getSelectedLanguage().sayPrompt("destination_noanswer")
    elif status in ["ANSWER"]:
        duration=ibs_agi.getAGI().get_variable("ANSWEREDTIME")
    elif status in ["CANCEL"]:
        pass

    if ibs_agi.getConfig().getValue("debug"):
        toLog("Dial: Status %s AnsweredTime %s"%(status,duration))

    ibs_agi.getConfig().setValue("authorized",False)
    
    return duration,status