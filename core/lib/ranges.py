"""
    Classes needed to handle and decompose range strings
    ranges are defines as {start-end} in strings
"""

import re
from core.errors import errorText
from core.ibs_exceptions import *


class RangeString:
    range_match=re.compile("({[nl]?[0-9]+-[0-9]+})")
    def __init__(self,string,left_pad=True):
        """
            "string" is raw String, we'll decompose this string to a list
            "string" may contain zero or more ranges, that will generate the final list of strings
        """
        self.string=string
        self.left_pad=left_pad
        raw_str_list=self.__decomposeString(string)
        iter_list=self.__createIterativeList(raw_str_list)
        self.all_strings=self.__createList(iter_list)

    def __iter__(self):
        return iter(self.all_strings)
        
    def __in__(self,obj):
        return obj in self.all_strings

    def __len__(self):
        return len(self.all_strings)

    def __getitem__(self,_index):
        return self.all_strings[_index]

    def __decomposeString(self,string):
        """
            decompose the "string" and return a list, by spliting it into parts that are normal strings without
            ranges, or a single range
        """
        str_list=self.range_match.split(string)
        return str_list
    
    def __createIterativeList(self,str_list):
        """
            create a list from "str_list" strings, that each member supports iteration.
            this is done, by wrapping ranges into "Range" instances and normal strings into a tuple
        """
        return map(self.__createIterator,str_list)

    def __createIterator(self,_str):
        """
            create an iterator object from _str
        """
        if self.range_match.match(_str)!=None:
            return self.__createRangeObj(_str)
        else:
            return [_str]


    def __createRangeObj(self,raw_range):
        """
            create a range object from raw_range (ex. "{1-10}")
        """
        return Range(raw_range,self.left_pad)

    def __createList(self,iter_list):
        """     
            subsitute ranges in string with range_objs values and return a list of all strings that is produced
            by string and ranges
        """
        str_list=[""]
        for iter_obj in iter_list: #go through all ranges
            if iter_obj==[""]: #empty strings are produced by split and useless
                continue
            str_temp_list=[] #we can't change str_list in loop
            for incomplete_str in str_list: #produce all strings
                for _str in iter_obj:
                    str_temp_list.append("%s%s"%(incomplete_str,_str))
            str_list=str_temp_list
        return str_list

    
class Range:
    def __init__(self,raw_range,left_pad=True):
        """
            raw_range is a string like {1-10} that represents raw range
            left_pad(boolean): if set to true, all string within the range are left zero padded to length
                                of maximum range member
        """
        self.raw_range=raw_range
        self.left_pad=left_pad
        (start_str,end_str)=self.__decompose(raw_range)
        (start,end)=self.__findStartEnd(start_str,end_str)
        self.__checkStartEnd(start,end)

        int_range=self.__generateIntRange(start,end)

        if self.left_pad:
            self.__findRangeStrLength(start,end)
            self.range=self.__leftPadIntRange(int_range)
        else:
            self.range=map(str,int_range)

    def __iter__(self):
        return iter(self.range)
        
    def __len__(self):
        return len(self.range)

    def __getitem__(self,_index):
        return self.range[_index%len(self)] #ranges are round robin, we never raise an IndexError Exception

    def __findRangeStrLength(self,start,end):
        """
            find range variable length,
            for ex. if range is 300-1200, we must left pad 300 with a 0, and our length is 4
        """
        self.str_length=max(len(str(start)),len(str(end)))

    def __generateIntRange(self,start,end):
        """
            create self.range from start and end
        """
        return range(start,end+1)

    def __findStartEnd(self,start_str,end_str):
        """
            find start end numbers
        """
        try:
            start=int(start_str)
            end=int(end_str)
        except ValueError:
            raise GeneralException(errorText("GENERAL","RANGE_ERROR"))
        return (start,end)
        
    def __checkStartEnd(self,start,end):
        """
            check start and end varibales
        """
        
        if end<=start:
            raise GeneralException(errorText("GENERAL","RANGE_END_LESS_THAN_START")%self.raw_range)
    
        if start-end>1024*1024:
            raise GeneralException(errorText("GENERAL","RANGE_IS_TOO_LARGE")%self.raw_range)    
    
    def __decompose(self,raw_range):
        _range=raw_range[1:-1]
        if _range[0]=="n":
            self.left_pad=False
            _range=_range[1:]
        elif _range[0]=="l":
            self.left_pad=True
            _range=_range[1:]
        range_sp=_range.split("-")
        if len(range_sp)!=2:
            raise GeneralException(errorText("GENERAL","RANGE_ERROR"))
        start_str=range_sp[0]
        end_str=range_sp[1]
        return (start_str,end_str)

    def __leftPadNum(self,num):
        """
            return string representation of "num" with length "self.str_length",
            it would leftpad num with 0 if "num" string length is fewer than "self.str_length"
        """
        num_str=str(num)
        if len(num_str)>self.str_length:
            raise GeneralException(errorText("GENERAL","RANGE_ERROR"))
        
        while (len(num_str)<self.str_length): num_str="0%s"%num_str
        return num_str

    def __leftPadIntRange(self,int_range):
        """
            left pad nums in self.int_range with 0 until their length is self.str_length
            save em into self.range
        """
        return map(self.__leftPadNum,int_range)