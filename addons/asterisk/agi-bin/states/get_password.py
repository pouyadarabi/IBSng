import ibs_agi

def init():
    ibs_agi.getStateMachine().registerState("GET_PASSWORD",getPassword)

def getPassword():
    password=ibs_agi.getSelectedLanguage().sayPromptAndCollect("get_password", 
                                                               ibs_agi.getConfig().getValue("max_password_length"))
    ibs_agi.getConfig().setValue("password",password)
    return password