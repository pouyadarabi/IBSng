"""
    tc command line wrapper
"""
import re
from core.ibs_exceptions import *
from core.script_launcher import launcher_main


class TC:
    counters_pattern=re.compile("class htb 1:([0-9]+) .*\n Sent ([0-9]+) bytes ([0-9]+) pkts? .*\n( rate ([0-9]+)bit)?")
    def addQdisc(self,interface,*args):
        self.runTC("qdisc add dev %s %s"%(interface," ".join(args)))

    def delQdisc(self,interface,*args):
        self.runTC("qdisc del dev %s %s"%(interface," ".join(args)))

    def addClass(self,interface,*args):
        self.runTC("class add dev %s %s"%(interface," ".join(args)))

    def changeClass(self,interface,*args):
        self.runTC("class change dev %s %s"%(interface," ".join(args)))

    def delClass(self,interface,*args):
        self.runTC("class del dev %s %s"%(interface," ".join(args)))

    def addFilter(self,interface,*args):
        self.runTC("filter add dev %s %s"%(interface," ".join(args)))

    def delFilter(self,interface,*args):
        self.runTC("filter del dev %s %s"%(interface," ".join(args)))


    def runTC(self,command):
        ret_val=launcher_main.getLauncher().system(defs.BW_TC_COMMAND,command.split())
        if ret_val!=0:
            toLog("tc command '%s %s' returned non zero value %s"%(defs.BW_TC_COMMAND,command,ret_val),LOG_DEBUG)

    ########################################
    def getCounters(self,interface):
        """
            return dictionary in format {minor tc id: (transmitted bytes,transmitted pkts,rate in bytes)
        """
        output=self.getOutput("-s -d class list dev %s"%interface)
        return self.__parseCounters(output)
        
    def __parseCounters(self,output):
        groups=self.counters_pattern.findall(output)
        dic={}

        for _tuple in groups:
            if _tuple[4]=="":
                rate=0
            else:
                rate=int(_tuple[4])
            dic[int(_tuple[0])]=(int(_tuple[1]),int(_tuple[2]),rate)
        return dic

    def getOutput(self,command):
        fd=launcher_main.getLauncher().popen(defs.BW_TC_COMMAND,command.split())
        lines=fd.readlines()
        fd.close()
        return "".join(lines)
