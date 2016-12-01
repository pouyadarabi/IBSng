from core.ibs_exceptions import *
from core.lib.time_lib import *
import time

class Interval:
    """
        This class represent time intervals in multiple day of weeks
        intervals can't cross days
    """

    def __init__(self,day_of_week_container,start,end):
        """
            day_of_week_container(DayOfWeekContainer Instance)
            start(str)
            end(str)
        """
        self.dow_container=day_of_week_container
        self.start=Time(start)
        self.end=Time(end)
        
    def __lt__(self,other):
        """
            other can be either Interval instance or integer that is seconds from morning
            comparing is done, by comparing start_time of interval
        """
        if isinstance(other,Interval):
            return self.start<=other.start
        else:
            return self.getStartSeconds()<=other


    def __gt__(self,other):
        """
            other can be either Interval instance or integer that is seconds from morning
            comparing is done, by comparing end_time of interval
        """
        if isinstance(other,Interval):
            return self.end>other.end
        else:
            return self.getEndSeconds()>other
    
    def containsDay(self,_time):
        """
            return True if current interval contains day of _time
            _time(long): seconds from epoch
        """
        return self.__getDayOfWeek(_time) in self.dow_container

    def __getDayOfWeek(self,_time):
        """
            return integer representation of day of week
        """
        return time.localtime(_time)[6]
    
    def containsNow(self):
        """
            return True if this interval contains now
        """
        return self.containsTime(time.time())

    def containsTime(self,_time):
        """
            return True if this interval contains _time. Both Day, and Interval in day is checked
            _time(long): seconds from morning
        """
        secs=secondsFromMorning(_time)
        return self.containsDay(_time) and self>secs and self<secs #don't panic interval greater than is checked with start, and less than is checked with end time

    def getStartSeconds(self):
        """
            return start time number of seconds from 0:0
        """
        return self.start.getSecondsFromMorning()

    def getEndSeconds(self):
        """
            return end time number of seconds from 0:0
        """
        return self.end.getSecondsFromMorning()

    def hasOverlap(self,other_interval):
        """
            check if this interval has overlap with other_interval.
            Two intervals has conflict if they have overlap in times of same day
        """
        if self.dow_container.hasOverlap(other_interval.dow_container):
            if self.getStartSeconds() > other_interval.getStartSeconds() and other_interval.getEndSeconds() > self.getStartSeconds():
                return 1

            elif self.getStartSeconds() < other_interval.getStartSeconds() and self.getEndSeconds() > other_interval.getStartSeconds():
                return 1

            elif self.getStartSeconds() == other_interval.getStartSeconds():
                return 1

        return 0

