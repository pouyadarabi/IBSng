from core.bandwidth_limit import bw_main
import itertools

class UserLeaf:
    def __init__(self,leaf_obj,ip_addr,direction):
        """
            leaf_obj(Leaf instance):
            ip_addr(str): ip address of user
            direction(str): can be one of "send" or "receive"
        """
        self.leaf_obj=leaf_obj
        self.ip_addr=ip_addr
        self.direction=direction

        self.service_marks=None
        self.default_mark=None
        
        self.minor_ids=[]

        self.total_minor_id=None
        self.default_minor_id=None
        self.service_minor_ids=[]

    def getIP(self):
        return self.ip_addr
    
    def getDirection(self):
        return self.direction
    
    def getLeafObj(self):
        return self.leaf_obj

    def getTotalMinorTC_ID(self):
        return self.total_minor_id

    def getDefaultMinorTC_ID(self):
        return self.default_minor_id

    def getServiceMinorTC_IDs(self):
        return self.service_minor_ids

    def getInterfaceName(self):
        return self.getLeafObj().getInterfaceName()
    ##############################
    def __getNewMinorTC_ID(self):
        _id=self.getLeafObj().getInterface().getMinorIDPool().getID(1)[0]
        self.minor_ids.append(_id)
        return _id
    ##############################
    def getInfo(self):
        bytes,pkts,rate=self.getCounters()
        return {"leaf_name":self.getLeafObj().getLeafName(),
                "interface_name":self.getInterfaceName(),
                "pkts":float(pkts),
                "bytes":float(bytes),
                "rate":rate,
                "ip":self.getIP(),
                "direction":self.getDirection()}
        
        
    ##############################
    def getCounters(self):
        """
            return tuple of (bytes,packets,rate) for this user leaf
        """
        if self.getTotalMinorTC_ID()!=None:
            return self.__getCountersForID(self.getTotalMinorTC_ID())
        else:
            return self.__getCountersFromServices()

    def __getCountersForID(self,_id):
        return bw_main.getManager().getCounters(self.getInterfaceName(),_id)
        
    def __getCountersFromServices(self):
        bytes,pkts,rate=self.__getCountersForID(self.getDefaultMinorTC_ID())
        for service_id in self.getServiceMinorTC_IDs():
            tbytes,tpkts,trate=self.__getCountersForID(service_id)
            bytes+=tbytes
            pkts+=tpkts
            rate+=trate
        return bytes,pkts,rate
    
    ###############################
    def addToTC(self):
        self.__addClassesAndFilters()

    def __addClassesAndFilters(self):
        all_parent_id=self.__addTotalClass()
        services=self.getLeafObj().getServices()
        self.__setMarks(services)
        
        map(self.__addService,
            services,
            self.service_marks,
            itertools.repeat(all_parent_id,len(services)))
        self.__addDefaultClassAndFilter(self.default_mark,all_parent_id)
        
    def __setMarks(self,services):
        marks=bw_main.getMarkIDPool().getID(len(services)+1)
        self.default_mark=marks[0]
        self.service_marks=marks[1:]
        
        
    def __addService(self,leaf_service,mark_id,parent_id):
        """
            add service limit in "leaf_service"
            mark_id(int): mark number to user with iptables
            parent_id(int): parent minor id of class
        """
        minor_id=self.__getNewMinorTC_ID()
        self.service_minor_ids.append(minor_id)
        bw_main.getTCRunner().addClass(self.getLeafObj().getInterfaceName(),
                                       "parent 1:%s"%parent_id,
                                       "classid 1:%s"%minor_id,
                                       "htb",
                                       "rate %skbit"%leaf_service.getRate(),
                                       "ceil %skbit"%leaf_service.getCeil(),
                                       "quantum 3000")
        bw_main.getIPTablesRunner().addMark(mark_id,self.ip_addr,self.direction,leaf_service)
        bw_main.getTCRunner().addFilter(self.getLeafObj().getInterfaceName(),
                                        "protocol ip",
                                        "prio 1",
                                        "handle %s fw"%mark_id,
                                        "flowid 1:%s"%minor_id)
        

    def __addDefaultClassAndFilter(self,mark_id,parent_id):
        """
            add default service limit class
            mark_id(int): mark number to user with iptables
            parent_id(int): parent minor id of default class
        """
        minor_id=self.__getNewMinorTC_ID()
        self.default_minor_id=minor_id
        bw_main.getTCRunner().addClass(self.getLeafObj().getInterfaceName(),
                                       "parent 1:%s"%parent_id,
                                       "classid 1:%s"%minor_id,
                                       "htb",
                                       "rate %skbit"%self.getLeafObj().getDefaultRate(),
                                       "ceil %skbit"%self.getLeafObj().getDefaultCeil(),
                                       "quantum 3000")
        bw_main.getIPTablesRunner().addMark(mark_id,self.ip_addr,self.direction,None)
        bw_main.getTCRunner().addFilter(self.getLeafObj().getInterfaceName(),
                                        "protocol ip",
                                        "prio 1",
                                        "handle %s fw"%mark_id,
                                        "flowid 1:%s"%minor_id)
    
    def __addTotalClass(self):
        """
            add Total Limit class
        """
        if self.getLeafObj().getTotalRate()>=0:
            _id=self.__getNewMinorTC_ID()
            self.total_minor_id=_id
            bw_main.getTCRunner().addClass(self.getLeafObj().getInterfaceName(),
                                           "parent 1:%s"%self.getLeafObj().getParentNode().getTC_ID(),
                                           "classid 1:%s"%_id,
                                           "htb",
                                           "rate %skbit"%self.getLeafObj().getTotalRate(),
                                           "ceil %skbit"%self.getLeafObj().getTotalCeil(),
                                           "quantum 3000")

            all_parent_id=_id
        else:
            all_parent_id=self.getLeafObj().getParentNode().getTC_ID()
            
        return all_parent_id
    ##############################
    def delFromTC(self):
        """
            delete this leaf from tc
        """     
        self.__delFilters()
        self.__delClasses()
        self.__delMarks()
    
    def __delClasses(self):
        self.minor_ids.reverse()
        map(self.__delClass,self.minor_ids)
        self.getLeafObj().getInterface().getMinorIDPool().freeID(self.minor_ids)

    def __delClass(self,minor_id):
        bw_main.getTCRunner().delClass(self.getLeafObj().getInterfaceName(),
                                       "classid 1:%s"%minor_id)
        
    def __delFilters(self):
        map(self.__delFilter,self.service_marks)
        self.__delFilter(self.default_mark)

    def __delFilter(self,mark_id):
        bw_main.getTCRunner().delFilter(self.getLeafObj().getInterfaceName(),
                                        "protocol ip",
                                        "prio 1",
                                        "handle %s fw"%mark_id)
    
    def __delMarks(self):
        map(self.__delMark,self.service_marks,self.getLeafObj().getServices())
        self.__delMark(self.default_mark,None)
        bw_main.getMarkIDPool().freeID(self.service_marks+[self.default_mark])

    def __delMark(self,mark_id,leaf_service):
        bw_main.getIPTablesRunner().delMark(mark_id,self.ip_addr,self.direction,leaf_service)
