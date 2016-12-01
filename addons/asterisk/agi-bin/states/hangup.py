import ibs_agi

def init():
    ibs_agi.getStateMachine().registerState("HANGUP",hangup)

def hangup():
    return ibs_agi.getAGI().hangup()
