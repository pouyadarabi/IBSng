import ibs_agi
from lib.error import *

def init():
    ibs_agi.getStateMachine().registerState("CREDIT_ANNOUNCEMENT",creditAnnouncement)

def creditAnnouncement():
    try:
        credit=ibs_agi.getStateMachine().gotoState("GET_CURRENT_CREDIT")
    except IBSException:
        return
    return ibs_agi.getStateMachine().gotoState("SAY_REMAINING_CREDIT",credit)
