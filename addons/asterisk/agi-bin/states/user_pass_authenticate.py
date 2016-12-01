import ibs_agi

def init():
    ibs_agi.getStateMachine().registerState("USER_PASS_AUTHENTICATE",userPassAuthenticate)

def userPassAuthenticate():
    counter=0
    while counter<ibs_agi.getConfig().getValue("retry") and not ibs_agi.getConfig().getValue("authenticated"):
        username=ibs_agi.getStateMachine().gotoState("GET_USERNAME",counter)
        if username == "":
            ibs_agi.getStateMachine().gotoState("AUTHENTICATION_FAILED")
            
        password=ibs_agi.getStateMachine().gotoState("GET_PASSWORD")
        credit=ibs_agi.getStateMachine().gotoState("AUTHENTICATE",username,password)
        counter+=1

    if not ibs_agi.getConfig().getValue("authenticated"):
        ibs_agi.getStateMachine().gotoState("AUTHENTICATION_FAILED")

    return credit