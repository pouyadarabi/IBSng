import ibs_agi

def init():
    ibs_agi.getStateMachine().registerState("GET_USERNAME",getUsername)

def getUsername(authentication_counter):
    """
        ask for username, retry if no username entered. return username or empty string
    """
    counter=0
    username=""
    while username=="" and counter<ibs_agi.getConfig().getValue("retry"):
        counter+=1
        max_len=ibs_agi.getConfig().getValue("username_length")
        if authentication_counter:
            prompt="get_username_again"
        else:
            prompt="get_username"
        
        username=ibs_agi.getSelectedLanguage().sayPromptAndCollect(prompt,max_len)
        
    ibs_agi.getConfig().setValue("username",username)
    return username
