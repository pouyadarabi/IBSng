import ibs_agi

def init():
    ibs_agi.getStateMachine().registerState("GOODBYE_HANGUP",goodbyeHangup)

def goodbyeHangup():
    ibs_agi.getSelectedLanguage().sayFile("goodbye")
    return ibs_agi.getStateMachine().gotoState("HANGUP")
