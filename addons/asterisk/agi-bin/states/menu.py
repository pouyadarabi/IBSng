import ibs_agi
from lib.error import *

def init():
    ibs_agi.getStateMachine().registerState("MENU",menu)

def menu():
    while True:
        selection=ibs_agi.getStateMachine().gotoState("SAY_MENU")
    
        if selection=="": #timeout
            selection=ibs_agi.getAGI().wait_for_digit(5000)
            if selection=="":
                ibs_agi.getSelectedLanguage().sayPrompt("no_digit_entered")
                continue

        if ibs_agi.getConfig().getValue("debug"):
            toLog("Menu: Selected %s"%selection)

        if selection in "*#": #go and ask for destination again
            return

        try:
            new_state=ibs_agi.getSelectedLanguage().getMenuIndexState(int(selection))
        except (KeyError,ValueError):
            ibs_agi.getStateMachine().gotoState("BAD_MENU_SELECTION")
            continue
                
        ibs_agi.getStateMachine().gotoState(new_state)
