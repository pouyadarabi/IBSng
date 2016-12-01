#!/usr/bin/python

import urllib
from analyze_lib import *
from analyze_exceptions import *

############# standard indexies ########
TIMESTAMP = 0
URL = 1
ELAPSED = 2
BYTES = 3
MISSED = 4
SUCCESSFUL = 5
COUNT = 6
TYPE = -1

class ObjTypeFilter:
    """
        filter repeated records 
    """
    def __flushBuffer(self):
        self.last_record = [] #holds last record, befor save it
        self.result = []

    def __validateURL(self, url):
        protocol, path = urllib.splittype(url)  
        if protocol != 'urlparse':
            return True
            
        return False
        
        
    def Filter(self,records):
        self.__flushBuffer()
        if not records:
            if getConf('DEBUG'):
                toLog("Filter Called with empty records")
            return False
        
        for record in records:
            if self.__validateURL(record[URL]):
                self.__mergeRecords(record)

        self.__flushLastRecord(None)

        return self.result
    
    def __flushLastRecord(self, next_record):

        p1, h1, d1, f1 = splitUrl(self.last_record[URL])
        self.last_record[URL] = "%s%s%s"%(p1,h1,d1)
    
        self.last_record.pop(-1)
        self.result.append(self.last_record)
        
        self.last_record = next_record
    
    def __areMergeCapable(self, next, prev):
        """
            determine if two records are merge capable by
            checking object types and then urls(base url)
        """
        if next[URL] == prev[URL]:
            return True
        
        p1, h1, d1, f1 = splitUrl(prev[URL])
        p2, h2, d2, f2 = splitUrl(next[URL])

        if h1 == h2 and d1 == d2 and next[TYPE] != 'text/html':
            mergable=True
        else:
            mergable=False
    
        if getConf("DEBUG")==2:
            toLog("Are Mergable: p1: %s h1: %s d1: %s f1: %s p2: %s h2: %s d2: %s f2: %s , Result: %s"%(p1,h1,d1,f1,p2,h2,d2,f2,mergable))

        return mergable
        
    def __mergeRecords(self,next_record):
        """
            merge related records 
        """
        if not len(self.last_record):
            self.last_record = next_record
            return True
            
        elif(self.__areMergeCapable(next_record,self.last_record)):

            self.last_record[ELAPSED] += next_record[ELAPSED]
            self.last_record[BYTES] += next_record[BYTES]
            self.last_record[COUNT] += 1  #one more
            
            if next_record[SUCCESSFUL]:
                self.last_record[SUCCESSFUL][0] += 1
            else:
                self.last_record[SUCCESSFUL][1] += 1

            if next_record[MISSED]:
                self.last_record[MISSED][0] += 1
            else:
                self.last_record[MISSED][1] += 1
                
        else:
            self.__flushLastRecord(next_record)
            
        
class LogPrepare(ObjTypeFilter):
    """
        for each user_ip return sorted records by url
        Note: Before filter call.
    """       
    def __flushCache(self):
        self.cache = {}
    
    def __checkStatus(self,status_str):
        """
            return a list consist of SUCCESS/FAILURE and MISS/HIT
        """
        flags = {'0':False,'1':True, '2':True,'3':True, '4':False, '5':False, '6': True}
        st = status_str.split('/')
        successful = [1,0] #success,fail
        try:
            if not flags[st[1][0]]:
                successful = [0,1]
        except:
            logException()
        
        missed = [1,0] #miss,hit
        if st[0].find('HIT') != -1:
            missed = [0,1]
        
        if getConf("DEBUG") == 2:
            toLog("Check Status: st: %s missed: %s successful: %s"%(st, missed, successful))

        return (missed, successful)
            
    def prepare(self, data):
        """
            prepare data for filter,split them and dictionarize them
            return (dict): {'user_ip' : [[ record_details], ...]}
            (timestamp, user_ip, elapsed, bytes, url, missed, successful, count)
        """
        self.__flushCache()
        for item in data:
            splitted_str = item.split()
            _user_ip = splitted_str[2]                  # user_ip
            if not self.cache.has_key(_user_ip):
                self.cache[_user_ip] = []

            record = []

            record.append(splitted_str[0])              # timestamp
            record.append(splitted_str[6])      # url
            record.append(int(round(int(splitted_str[1])/1000.0)))              # elapsed time

            record.append(int(splitted_str[4]))         # bytes
            
            _missed, _success = self.__checkStatus(splitted_str[3]) # missed and successful
            record.append(_missed)
            record.append(_success)

            record.append(1) #count
            record.append(splitted_str[-1])     # object type
            
            self.cache[_user_ip].append(record)
            
        return self.__callFilter()

    def __callFilter(self):
        """
            returns a dictionary that all related urls
            are behind each other for each user ip
        """
        checked_urls  =[]
        filtered_dict = {}
        for user_ip in self.cache:
            ret = self.__sort(self.cache[user_ip])
            ret = self.Filter(ret)
            
            filtered_dict[user_ip] = ret       
        return filtered_dict
        
    def cmpFunct(self,l1,l2):
        return cmp(l1[URL], l2[URL])
        
    def __sort(self, big_list):
        big_list.sort(self.cmpFunct)
        return big_list
