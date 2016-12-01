import ibs_agi
from lib.error import *

def init():
    ibs_agi.getStateMachine().registerState("CONFIRM_FAST_DIAL",confirmFastDial)

def confirmFastDial(_index,destination):
    for f in [lambda:ibs_agi.getSelectedLanguage().sayPrompt("pre_confirm_fast_dial"),
              lambda:ibs_agi.getSelectedLanguage().sayDigit(_index),
              lambda:ibs_agi.getSelectedLanguage().sayPrompt("mid_confirm_fast_dial"),
              lambda:ibs_agi.getSelectedLanguage().sayDigits(destination),
              lambda:ibs_agi.getSelectedLanguage().sayPrompt("post_confirm_fast_dial"),
              ]:
        digit=f()
        if digit:
            return digit

    return ibs_agi.getAGI().wait_for_digit(3000)