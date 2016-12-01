import time
import threading

from core.ibs_exceptions import *
from core.event import periodic_events
from radius_server import rad_main

class RequestList:
    """
        RequestList is list of recieved radius requests, and response of them
        this list is used to check for duplicate requests
    """
    def __init__(self):
        self.__requests = {} # (src_ip, src_port, id) => Request Instance 
        self.__cleanup_lock = threading.Lock()
    
    def __generateKey(self, pkt):
        """
            return key for dictionary lookup of pkt
        """
        src_ip, src_port = pkt.source
        return (src_ip, src_port, pkt.id, pkt.code)
    
    def addRequest(self, request_pkt):
        """
            add a new request to RequestList
        """
        key = self.__generateKey(request_pkt)

        self.__cleanup_lock.acquire()
        try:
            self.__requests[key] = Request(request_pkt)
        finally:
            self.__cleanup_lock.release()
    
    def getRequest(self, request_pkt):
        """
            return Request object if exists
            return None if Request doesn't exists here
        """
        key = self.__generateKey(request_pkt)
        
        try:

            if self.__requests.has_key(key): #this is faster than try/expect
                return self.__requests[key]
            return None

        except KeyError: #rare race condition
            return None

    def cleanup(self):
        """
            cleanup older than one minute requests
        """
        
        self.__cleanup_lock.acquire()
        try:
            to_delete_keys = []
    
            min_time = long(time.time()) - defs.RADIUS_SERVER_CLEANUP_TIME
            for key in self.__requests:
                request_obj = self.__requests[key]

                if request_obj.getStartTime() < min_time: 
                    to_delete_keys.append(key)

                    if not request_obj.isFinished():
                	toLog("WARNING: Unfinished request for 1 minute key: %(key)s"%locals(), LOG_ERROR)
                
            for key in to_delete_keys:
                del(self.__requests[key])

        finally:
            self.__cleanup_lock.release()


class Request:
    def __init__(self, request_pkt):
        self.request_pkt = request_pkt
        self.response_pkt = None
        
        self.start = time.time()
        self.finish = None

    def isFinished(self):
        """
            return True if this request is already replied
        """
        return self.response_pkt != None

    def getStartTime(self):
        return self.start

    def getRequestPacket(self):
        return self.request_pkt
    
    def getResponsePacket(self):
        return self.response_pkt

    def setResponsePacket(self, response_pkt):
        self.response_pkt = response_pkt
        self.finish = time.time()


class CleanRequestListPeriodicEvent(periodic_events.PeriodicEvent):
    def __init__(self):
        periodic_events.PeriodicEvent.__init__(self, "request_list_cleanup", defs.RADIUS_SERVER_CLEANUP_TIME, [], False)
    
    def run(self):
        rad_main.getRequestList().cleanup()
