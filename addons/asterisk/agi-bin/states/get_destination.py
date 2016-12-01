import ibs_agi

def init():
    ibs_agi.getStateMachine().registerState("GET_DESTINATION",getDestination)

def getDestination(repeat=False,retry=0):
    """
        get destination and return it. return '*' if user requested to goto the menu
    """
    end_of_collect="#"
    request_redial="*"
    max_digits=ibs_agi.getConfig().getValue("max_destination_digits")
    timeout=4000
    
    destination=""
    if repeat: #are we trying to redial?
        digit=ibs_agi.getSelectedLanguage().sayPrompt("get_destination_again")
    else:
        digit=ibs_agi.getSelectedLanguage().sayPrompt("get_destination")
    if digit=="*":
        return digit
    else:
        while len(destination)<max_digits:
            destination+=digit
            digit=ibs_agi.getAGI().wait_for_digit(timeout)
            if not digit: #timeout
                if destination:
                    break
                else:
                    retry+=1
                    if retry<ibs_agi.getConfig().getValue("retry"):
                        return getDestination(repeat, retry)
                    else:
                        return ""
            elif destination=="" and digit=="*":
                return "*"
            elif digit==request_redial:
                return getDestination(True)
            elif digit==end_of_collect:
                break
                
        return destination
        
    