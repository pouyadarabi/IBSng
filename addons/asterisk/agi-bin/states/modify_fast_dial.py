import ibs_agi

def init():
    ibs_agi.getStateMachine().registerState("MODIFY_FAST_DIAL",modifyFastDial)

def modifyFastDial():
    """
    """
    _index=ibs_agi.getStateMachine().gotoState("GET_FAST_DIAL_INDEX")
    if not _index or not _index.isdigit(): #timeout or #*
        return
    
    destination=ibs_agi.getStateMachine().gotoState("GET_FAST_DIAL_DIGITS",_index)
    if destination in ["*",""]:
        return

    ibs_agi.getStateMachine().gotoState("ADD_DESTINATION_TO_FAST_DIAL",_index,destination)
    
    



