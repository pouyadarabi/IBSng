import ibs_agi
from lib.error import *

def init():
    ibs_agi.getStateMachine().registerState("GET_FAST_DIAL_INDEX",getFastDialIndex)

def getFastDialIndex():
    _index=""
    counter=0
    while _index=="" and counter<ibs_agi.getConfig().getValue("retry"):
        counter+=1
        _index=ibs_agi.getSelectedLanguage().sayPrompt("enter_fast_dial_index")
        if not _index:
            _index=ibs_agi.getAGI().wait_for_digit(3000)

    return _index