import ibs_agi
from lib.error import *

def init():
    ibs_agi.getStateMachine().registerState("CHANGE_PASSWORD",changePassword)

def changePassword():
    old_password=ibs_agi.getStateMachine().gotoState("GET_OLD_PASSWORD")
    if not old_password:
        return
        
    pass_correct=ibs_agi.getStateMachine().gotoState("CHECK_OLD_PASSWORD", old_password)
    if pass_correct:    
        new_password=ibs_agi.getStateMachine().gotoState("GET_NEW_PASSWORD")
        if not new_password:
            return

        ibs_agi.getStateMachine().gotoState("CHANGE_TO_NEW_PASSWORD", new_password)
