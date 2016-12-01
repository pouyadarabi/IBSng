import threading
import time
import resource
import os

from core import main

class StatKeeper:
    def __init__(self):
        self.__stats = {} #stat_name:[value,type]

        self.__lock = threading.RLock()

    def registerStat(self, stat_name, _type, initial_value = 0):
        """
            _type(str): type of value for this statistic.
                        candidates are "seconds" "int" "bytes" "string"
                        this is used by interface to show the statistic
        """
        self.__stats[stat_name] = [initial_value, _type]

    def inc(self, stat_name, amount = 1):
        """
            increment amount of state_name by amount
        """
        self.__lock.acquire()
        try:
            self.__stats[stat_name][0] += amount
        finally:
            self.__lock.release()

    def getValue(self, stat_name):
        return self.__stats[stat_name][0]

    def max(self, stat_name, value):
        """
            set stat_name value as maximum of "value" and current value
        """
        self.__lock.acquire()
        try:
            self.__stats[stat_name][0] = max(value, self.__stats[stat_name][0])
        finally:
            self.__lock.release()


    def avg(self, avg_stat_name, count_stat_name, value):
        """
            add new value to average of stat_name
            avg_stat_name is name of average stat
            count_stat_name is name of stat_name which count is stored, this stat is incremented by one
        """
        self.__lock.acquire()
        try:
            self.inc(count_stat_name)
            self.__stats[avg_stat_name][0] = (self.__stats[avg_stat_name][0] * (self.__stats[count_stat_name][0] - 1) + value) / self.__stats[count_stat_name][0]
        finally:
            self.__lock.release()

    def getStats(self):
        """
            Get a dictionary of statistics.
        """
        self.__updateStats()
        return self.__stats

    def __updateStats(self):
        """
            update statistices to laters
            uptime and some usages are magically added here
        """
        self.__stats["uptime"] = [time.time() - main.getStartTime(), "seconds"]
        self.__stats["memory_usage"] = [self.__getMemUsage(), "bytes"]
        self.__stats["load_avg"] = [self.__getLoadAvg(), "string"]
        

    def __getLoadAvg(self):
        """
            return load average for last 1 minute

            NOTE: Only works on linux
        """
        try:
            fd = open("/proc/loadavg")
            content = fd.read()
            fd.close()
        
            return content.split()[0]       
        except:
            logException(LOG_DEBUG)
            return 0.0

    def __getMemUsage(self):
        """
            return resident size of current process in bytes
            
            NOTE: Only works on linux
        """
    
        scale = {'kb': 1024.0, 'mb': 1024.0*1024.0}
        
        try:
            fd = open("/proc/%s/status"%os.getpid())
            content = fd.read()
            fd.close()
        except:
            logException(LOG_DEBUG)
            return 0.0  # non-Linux?     
        
        i = content.index("VmRSS")    
        rss = content[i:].split(None, 3)
        if len(rss) < 3:        
            return 0.0  # invalid format?     

        # convert Vm value to bytes    
        return float(rss[1]) * scale[rss[2].lower()]