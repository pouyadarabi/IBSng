"""
    classes to handle multiple strings in one!
    they are strings that composed of multiple ranges (see ranges.py) or normal strings (1 length range string)
    they are delimited by "," such as "apple,orange,banana"
    multi_strs return the last index value, if index is too big.
    negative indexes are not allowed
"""

from core.lib import ranges
import itertools

class MultiStr:
    def __init__(self,string,left_pad=True):
        self.string=string
        self.left_pad=left_pad
        sp_strs=self.__splitMulti()
        self.ranges_list=self.__createRangeList(sp_strs)
        self._len=self.__calculateLength()

    def __len__(self):
        return self._len
        
    def __calculateLength(self):
        return reduce(lambda sum,range_str:sum+len(range_str),self.ranges_list,0)
    
    def __getitem__(self,_index):
        if _index<0:
            raise IndexError("MultiStr index out of range")
        elif _index>=len(self):
            _index=len(self)-1
        sum=0
        for _range in self.ranges_list:
            sum+=len(_range)
            if sum>_index:
                return _range[_index-(sum-len(_range))]

    def __getslice__(self, s, e):
        return [self[i] for i in range(s,min(e,len(self)))]

    def __iter__(self):
        class MultiStrIter:
            def __init__(mself,multi_str_obj):
                mself.cur_index=0
                mself.multi_str_obj=multi_str_obj
                mself.last_range=None
                mself.last_range_index=-1
                mself.last_sum=0
        
            def __iter__(mself):
                return mself
        
            def next(mself):
                if mself.cur_index>=len(mself.multi_str_obj):
                    raise StopIteration()
    
                if mself.last_sum<=mself.cur_index or mself.last_sum==0:
                    mself.last_range_index+=1
                    mself.last_range=mself.multi_str_obj.ranges_list[mself.last_range_index]
                    mself.last_sum+=len(mself.last_range)

                range_index=mself.cur_index-(mself.last_sum-len(mself.last_range))
                mself.cur_index+=1
#               print str(mself.last_sum),str(mself.cur_index),str(len(mself.last_range)),str(range_index)
                return mself.last_range[range_index]
                
        return MultiStrIter(self)
            
    
    def __splitMulti(self):
        """
            split multistring into it's primitives
        """
        return self.string.split(",")
    
    def __createRangeList(self,sp_strs):
        """
            sp_strs(list of string): list of multi_str members
            create a list of ranges from multistring members,
            ranges_list would be a list of RangeString instances
        """
        return map(self.__createRangeString,sp_strs)

    def __createRangeString(self,_str):
        """
            create a RangeString instance of _str
        """
        return ranges.RangeString(_str,self.left_pad)
