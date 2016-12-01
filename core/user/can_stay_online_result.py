from core import defs
import sys

class CanStayOnlineResult:
    MIN_REMAINING_TIME=30
    DEBUG=False
    
    def __init__(self):
        self.remaining_time = sys.maxint
        self.kill_dic = {}#{instance:"kill_reason"}

    def getRemainingTime(self):
        return self.remaining_time

    def getEventTime(self):
        remaining_time = self.getRemainingTime()

        if self.DEBUG:
            print "Return Next Event: %s"%remaining_time

        if remaining_time != 0 and remaining_time < self.MIN_REMAINING_TIME:
            return self.MIN_REMAINING_TIME

        return remaining_time

    def getKillDic(self):
        return self.kill_dic

    def __add__(self,can_stay_online_result):
        """
            merge this object with another can_stay_online object.
            this is done, by choosing minimum remaining_time and merge kill_dic
        """
        self.setNew(can_stay_online_result.getRemainingTime(),can_stay_online_result.getKillDic())
        return self

    def setNew(self,remaining_time,kill_dic):
        """
            add new values to object, by calling self.newRemainingTime and self.addInstanceToKill
        """
        self.newRemainingTime(remaining_time)
        self.__mergeKillDic(kill_dic)

    def setKillForAllInstances(self,kill_reason,instances):
        """
            set kill for all instances of user with reason "kill_reason"
            returned remaining time will be set to 0, so no new event for user will set
        """
        self.newRemainingTime(0) #zero means no more next events
        for instance in range(1,instances + 1):
            self.addInstanceToKill(instance,kill_reason)

    def newRemainingTime(self,new_remaining_time):
        """
            new_remaining_time(integer): new calculated remaining time in seconds
            add another remaining time to object. we check the new remaining time
            against previous remaining times, and choose the minimum
            
            NOTE: zero remaining_time means no next remaining_time
        """
        if self.DEBUG:
            print "New Remaining time: %s"%new_remaining_time
            
        self.remaining_time=min(self.remaining_time, new_remaining_time)
    
    def addInstanceToKill(self, instance, kill_reason):
        """
            instance(integer): instance of user
            kill_reason(text): reason of killing user
            add a new instance to kill.
        """
        if self.kill_dic.has_key(instance):
            self.kill_dic[instance]="%s, %s"%(self.kill_dic[instance],kill_reason)
        else:
            self.kill_dic[instance]=kill_reason
    
    
    def __mergeKillDic(self,kill_dic):
        for instance in kill_dic:
            self.addInstanceToKill(instance,kill_dic[instance])

            
