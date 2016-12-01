import ibs_agi

def init():
    ibs_agi.getStateMachine().registerState("MAIN",main)

def main():
    ibs_agi.getStateMachine().gotoState("SET_SESSION_VARIABLES")
    credit=ibs_agi.getStateMachine().gotoState("CALLERID_AUTHENTICATE")
    ibs_agi.getStateMachine().gotoState("GREETING")
    ibs_agi.getStateMachine().gotoState("CHOOSE_LANGUAGE")
    if not ibs_agi.getConfig().getValue("authenticated"):
        credit=ibs_agi.getStateMachine().gotoState("USER_PASS_AUTHENTICATE")
    
    ibs_agi.getStateMachine().gotoState("SAY_REMAINING_CREDIT",credit)
    
    
    while True:
        destination=ibs_agi.getStateMachine().gotoState("GET_DESTINATION")
        if destination=="*":
            ibs_agi.getStateMachine().gotoState("MENU")
        elif destination=="":
            ibs_agi.getStateMachine().gotoState("GOODBYE_HANGUP")
        else:
            ibs_agi.getStateMachine().gotoState("DIAL",destination)     