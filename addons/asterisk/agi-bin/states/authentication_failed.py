import ibs_agi
from lib.error import *

def init():
    ibs_agi.getStateMachine().registerState("AUTHENTICATION_FAILED",authenticationFailed)

def authenticationFailed():
    ibs_agi.getSelectedLanguage().sayPrompt("authentication_failed")
    ibs_agi.getStateMachine().gotoState("GOODBYE_HANGUP")
    raise IBSException("Authentication Failed")
