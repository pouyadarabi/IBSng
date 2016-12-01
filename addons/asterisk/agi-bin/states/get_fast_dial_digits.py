import ibs_agi
from lib.error import *

def init():
    ibs_agi.getStateMachine().registerState("GET_FAST_DIAL_DIGITS",getFastDialDigits)

def getFastDialDigits(_index,retry=0):
    for f in [lambda:ibs_agi.getSelectedLanguage().sayPrompt("pre_get_fast_dial_destination"),
              lambda:ibs_agi.getSelectedLanguage().sayDigit(_index),
              lambda:ibs_agi.getSelectedLanguage().sayPrompt("post_get_fast_dial_destination")]:
        digit=f()
        if digit:
            break
    
    end_of_collect="#"
    request_recollect="*"
    max_digits=ibs_agi.getConfig().getValue("max_destination_digits")
    timeout=4000
    
    digits=""
    
    while len(digits)<max_digits:
        digits+=digit
        digit=ibs_agi.getAGI().wait_for_digit(timeout)
        if not digit: #timeout
            if digits:
                break
            else:
                retry+=1
                if retry<ibs_agi.getConfig().getValue("retry"):
                    return getFastDialDigits(_index,retry)
                else:
                    return ""
        elif digits=="" and digit=="*":
            return "*"
        elif digit==request_recollect:
            return getFastDialDigits(_index)
        elif digit==end_of_collect:
            break
                
    return digits
