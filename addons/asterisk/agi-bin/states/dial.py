import ibs_agi
from lib.error import *

def init():
    ibs_agi.getStateMachine().registerState("DIAL",dial)

def dial(destination):
    duration=0
    status="HANGUP"
    do_call_end=True
    authorized=False
    try:
        remaining_time=ibs_agi.getStateMachine().gotoState("AUTHORIZE",destination)
            
        if ibs_agi.getConfig().getValue("authorized"):
            ibs_agi.getStateMachine().gotoState("SAY_REMAINING_TIME",remaining_time)
            (duration,status)=ibs_agi.getStateMachine().gotoState("DIAL_DESTINATION",destination, remaining_time)
        else:
            do_call_end=False
            return
    finally:
        if do_call_end:
            (duration,used_credit)=ibs_agi.getStateMachine().gotoState("CALL_END",duration,status)

            ch_status=ibs_agi.getAGI().channel_status()
            if ibs_agi.getConfig().getValue("debug"):
                toLog("AferDial ChannelStatus: "+str(ch_status))

            ibs_agi.getStateMachine().gotoState("SAY_USED_CREDIT",duration,used_credit)
