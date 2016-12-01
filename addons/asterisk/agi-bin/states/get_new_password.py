import ibs_agi

def init():
    ibs_agi.getStateMachine().registerState("GET_NEW_PASSWORD",getNewPassword)

def getNewPassword():
    """
    """
    new_password=ibs_agi.getSelectedLanguage().sayPromptAndCollect("get_new_password",
                                                                   ibs_agi.getConfig().getValue("max_password_length"))
    if not new_password:
        ibs_agi.getSelectedLanguage().sayPrompt("no_digit_entered")
    return new_password    
    
        
    