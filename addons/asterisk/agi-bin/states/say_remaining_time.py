import ibs_agi
from lib import request

def init():
    ibs_agi.getStateMachine().registerState("SAY_REMAINING_TIME",sayRemainingTime)

def sayRemainingTime(seconds):
    for f in [lambda:ibs_agi.getSelectedLanguage().sayPrompt("pre_say_remaining_time"),
              lambda:ibs_agi.getSelectedLanguage().sayTime(seconds),
              lambda:ibs_agi.getSelectedLanguage().sayPrompt("post_say_remaining_time")]:
              
              ret = f()
              if ret:
                return ret
    
    