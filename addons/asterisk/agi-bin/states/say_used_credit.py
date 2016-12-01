import ibs_agi
from lib import request

def init():
    ibs_agi.getStateMachine().registerState("SAY_USED_CREDIT",sayUsedCredit)

def sayUsedCredit(duration, used_credit):

    if duration:
        for f in [lambda:ibs_agi.getSelectedLanguage().sayPrompt("pre_say_talked_duration"),
                  lambda:ibs_agi.getSelectedLanguage().sayTime(duration),
                  lambda:ibs_agi.getSelectedLanguage().sayPrompt("post_say_talked_duration")]:

            ret = f()
            if ret:
                return ret
              
    for f in [lambda:ibs_agi.getSelectedLanguage().sayPrompt("pre_say_used_credit"),
              lambda:ibs_agi.getSelectedLanguage().sayCredit(int(used_credit)),
              lambda:ibs_agi.getSelectedLanguage().sayPrompt("post_say_used_credit")]:
              
              ret = f()
              if ret:
                return ret
    
    