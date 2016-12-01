from core.ibs_exceptions import *
from threading import RLock

class IDPool:
    def __init__(self,_range,name):
        """
            range(list): initialize free range with this value
        """
        self.lock=RLock()
        self.__free_ranges=[]
        self.__insertToFreeRanges(_range)
        self.name=name

    def __getIDsFromRange(self,_count,_range):
        if _range[0]+_count<=_range[1]:
            return range(_range[0],_range[0]+_count)
        else:
            return range(_range[0],_range[1]+1)
        
    def __insertToFreeRanges(self,new_range):
        i=0
        new_range=list(new_range)
        self.lock.acquire()
        try:
            for _range in self.__free_ranges:
                if _range[0]>new_range[0]:
#                   self.printPool()
                    backward_merge=False
                    forward_merge=False
                    if i>0 and self.__free_ranges[i-1][1]+1==new_range[0]:
                        self.__free_ranges[i-1][1]=new_range[1]
                        backward_merge=True
                
                    if i<len(self.__free_ranges) and self.__free_ranges[i][0]-1==new_range[1]:
                        self.__free_ranges[i][0]=new_range[0]
                        forward_merge=True
                
                    if backward_merge and forward_merge:
                        self.__free_ranges.insert(i,[self.__free_ranges[i-1][0],self.__free_ranges[i][1]])
                        del(self.__free_ranges[i-1])
                        del(self.__free_ranges[i])
                    elif not backward_merge and not forward_merge:
                        self.__free_ranges.insert(i,new_range)
                    return
                i+=1
            self.__free_ranges.insert(i-1,new_range)
        finally:
            self.lock.release()
        
    def __popFreeRange(self):
        if len(self.__free_ranges)==0:
            raise GeneralException("No ID is available from pool %s"%self.name)
        return self.__free_ranges.pop(0)

    def getID(self,_count):
        """
            return _count number of free id's in a list
        """
        ids=[]
        while len(ids)!=_count:
            free_range=self.__popFreeRange()
            ids.extend(self.__getIDsFromRange(_count,free_range))

        if ids[-1]!=free_range[1]:
            self.__insertToFreeRanges([ids[-1]+1,free_range[1]])
        return ids              

    def freeID(self,ids):
        """
            ids(list): list of ids to be freed
        """
        ids.sort()
        _ranges=self.__convertToRanges(ids)
        map(self.__insertToFreeRanges,_ranges)

    def __convertToRanges(self,ids):
        _ranges=[]
        i=1
        range_begin=ids[0]
        for _id in ids[1:]:
            if _id!=ids[i-1]+1:
                _ranges.append([range_begin,ids[i-1]])
                range_begin=_id
            i+=1
        _ranges.append([range_begin,ids[-1]])
        return _ranges

    def printPool(self):
        print self.__free_ranges

"""
def test():
    pool=IDPool((0,10000),"test")
    f1=pool.getID(10)
    f2=pool.getID(10)
    f3=pool.getID(10)
    pool.printPool()
    pool.freeID(f1)
    pool.printPool()
    pool.freeID(f3)
    pool.printPool()
    pool.freeID(f2)
    pool.printPool()
    print "-----------------"
    import random
    ids=[]
    for i in range(100):
        ids.append(pool.getID(random.randrange(1,100)))
    pool.printPool()
    random.shuffle(ids)
    for ii in ids:
        pool.freeID(ii)
    pool.printPool()
"""
    