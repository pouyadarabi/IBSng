import ibs_agi
from lib.error import *

def init():
    ibs_agi.getStateMachine().registerState("FAST_DIAL",fastDial)

def fastDial():
    """
    """
    while True:
        _index=ibs_agi.getStateMachine().gotoState("GET_FAST_DIAL_INDEX")
        if not _index or not _index.isdigit(): #timeout or #*
            return
    
        try:
            destination=ibs_agi.getStateMachine().gotoState("GET_FAST_DIAL_DESTINATION_FROM_IBS",_index)
        except IBSException:
            return 
    
        if destination == "":
            return ibs_agi.getSelectedLanguage().sayPrompt("destination_incorrect")

        confirm=ibs_agi.getStateMachine().gotoState("CONFIRM_FAST_DIAL",_index,destination)
        if confirm==_index:
            return ibs_agi.getStateMachine().gotoState("DIAL",destination)
    
    



