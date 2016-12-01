import ibs_agi
from lib.error import *


class StateMachine:
    def __init__(self,initial_state):
        self.states={} #state_name:callable_object
        self.cur_state=initial_state

    def registerState(self, state_name, callable_obj):
        self.states[state_name]=callable_obj
        
    def __getState(self, state_name):
        return self.states[state_name]

    def gotoState(self, state_name, *args):
        """     
            change state to state_name, passing args to new state method
            after state method returns, last state will be recovered
        """
        if ibs_agi.getConfig().getValue("debug"):
            toLog("StateMachine: Going to state %s %s"%(state_name,args))

        last_state=self.cur_state
        self.cur_state=state_name
        try:
            ret_val=apply(self.__getState(state_name),args)
        except KeyError:
            toLog("StateMachine: State %s not found"%state_name)
            ret_val == None
            
        self.cur_state=last_state
        return ret_val
    
    def start(self):
        return apply(self.states[self.cur_state],[])
