import ibs_agi
from lib import request

def init():
    ibs_agi.getStateMachine().registerState("SAY_REMAINING_CREDIT",sayRemainingCredit)

def sayRemainingCredit(credit):
    for f in [lambda:ibs_agi.getSelectedLanguage().sayPrompt("pre_say_remaining_credit"),
              lambda:ibs_agi.getSelectedLanguage().sayCredit(credit),
              lambda:ibs_agi.getSelectedLanguage().sayPrompt("post_say_remaining_credit")]:
              
              ret = f()
              if ret:
                return ret
    
    