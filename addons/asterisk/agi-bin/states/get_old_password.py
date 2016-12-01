import ibs_agi

def init():
    ibs_agi.getStateMachine().registerState("GET_OLD_PASSWORD",getOldPassword)

def getOldPassword():
    """
    """
    old_password=ibs_agi.getSelectedLanguage().sayPromptAndCollect("get_old_password",
                                                                   ibs_agi.getConfig().getValue("max_password_length"))
    if not old_password:
        ibs_agi.getSelectedLanguage().sayPrompt("no_digit_entered")
        
    return old_password
    
        
    