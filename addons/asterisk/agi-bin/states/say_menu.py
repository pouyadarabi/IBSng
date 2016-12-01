import ibs_agi
from lib import request

def init():
    ibs_agi.getStateMachine().registerState("SAY_MENU",sayMenu)

def sayMenu():
    return ibs_agi.getSelectedLanguage().sayMenu()