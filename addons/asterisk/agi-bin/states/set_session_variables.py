import ibs_agi
import re

filter_caller_id_match = re.compile("[^a-zA-Z0-9+]")

def init():
    ibs_agi.getStateMachine().registerState("SET_SESSION_VARIABLES",setSessionVariables)

def setSessionVariables():
    caller_id = filter_caller_id_match.sub("", ibs_agi.getAGI().env["agi_callerid"])
    ibs_agi.getConfig().setValue("caller_id", caller_id)
    ibs_agi.getConfig().setValue("unique_id", ibs_agi.getAGI().env["agi_uniqueid"])
    ibs_agi.getConfig().setValue("channel", ibs_agi.getAGI().env["agi_channel"])
