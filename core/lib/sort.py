class SortedList:
    def __iter__(self):
        return iter(self.list)

    def __getitem__(self,_index):
        return self.list[_index]
    
    def __init__(self,list):
        self.list=list

    def sortByIndex(self,_index,desc):
        """
            Sort list by value of objects of index of list !
            list should be a list of lists then
        """
        return self.__sortByIndex(_index, desc)

    def sortByPostText(self,post_text,desc):
        """
            Sort list using post_text after each item of list
            ex. if list is [[1,2,3],[2,3,4]] and we want to sort the list with first item of
            each member, post_text is "[0]" so for each member we compare m[0]s
        """
        
        return self.__sortByPostText(post_text, "", desc)

    def sortByValueDicKey(self, value_key, desc):
        """
            if list members are dictionaries, sort them by "value_key" of dictionary
            this is faster than using sortByPostText
        """
        self.__sortByValueKey(value_key, desc)

    def sort(self, desc):
        """
            sort the internal list
            desc show descending flag
        """
        self.__sortByIndex(0, desc)

    def __sort(self, _list, _index, desc, pop_first_element=False):
        """
            sort "_list" by "_index" of each member
            
            pop_first_element(bool): if set to True first element of _list will be removed
                                     after sort is done
        """
        if _index != 0:
            _list = [(x[_index], x) for x in _list]
        
        _list.sort()
        
        if desc:
            _list.reverse()

        if _index != 0 or pop_first_element: 
            _list = [x[1] for x in _list]

        return _list
        
    def __sortByIndex(self, _index, desc):
        self.list = self.__sort(self.list, _index, desc)
        
    def __sortByPostText(self,post_text,pre_text,desc):
        _list = []
        
        for x in self.list:
            try:
                _list.append( (eval("%sx%s"%(pre_text,post_text)), x) )
            except KeyError:
                _list.append( (-1, x) )
        
        self.list = self.__sort(_list, 0, desc, True)
        
    def __sortByValueKey(self, value_key, desc):
        _list = [(x.get(value_key, -1),x) for x in self.list]
        self.list = self.__sort(_list, 0, desc, True)

    def getList(self):
        """
            get sorted list after calling self.sort* methods
        """
        return self.list            


class SortedDic:
    def __init__(self,dic):
        self.dic=dic
        self.sorted_list=SortedList(self.__dic2list(dic))
    
    def __dic2list(self,dic):
        """
            convert the dic into a list by creating and array and put the key of dic in first index and
            dic value in second index
            summary: {x:y,z:c}->[[x,y],[z,c]]
        """
        return [(x,dic[x]) for x in dic]

    def sortByKey(self, desc):
        self.sorted_list.sortByIndex(0, desc)
        
    def sortByValue(self, desc):
        self.sorted_list.sortByIndex(1, desc)

    def sortByPostText(self,post_text,desc):
        self.sorted_list.sortByPostText(post_text,desc)    

    def getList(self):
        """
            return sorted list produced from dic. to understand list format see __dic2list
        """
        return self.sorted_list.getList()

####NOT CHECKED
        
def sortListWithHash(list,order_by,order_by_hash,default,desc):
    """
        sort "list" by "order_by" using "order_by_hash" to determine index or "postText"
        "order_by_hash" is a hash in format {order_by_name=>postText of list}
        ex. list is [[index,connect_time],...] order_by_hash {index:"[0]",connect_time:"[1]"}
        default is used if "order_by" argument is not in "order_by_hash" hash
        desc is a boolean "0" or "1"
    """
    if order_by_hash.has_key(order_by):
        return sortList(list,order_by_hash[order_by],"",desc)
    else:
        return sortList(list,order_by_hash[default],"",desc)

if __name__ == "__main__":
    import timeit
    import random
    
    def createDic():
        _dic={}
        for i in xrange(10000):
            _dic[random.random()*10000] = {1:random.random()*10000}
    
        return _dic

    def createList():
        _list = []

        for i in xrange(10000):
            _list.append({1:random.random()*10000})

        return _list
        
    def sortDic():
        _dic=createDic()
        s=SortedDic(_dic)
#       s.sortByKey(1)
        s.sortByPostText("[1][1]", True)

    def sortList():
        _list=createList()
        s=SortedList(_list)
        s.sortByValueDicKey(1, True)
#       s.sortByPostText("[1]", True)
    
    
#    t=timeit.Timer("sortDic()","from __main__ import sortDic")
#    print t.timeit(number=10)
    t=timeit.Timer("sortList()","from __main__ import sortList")
    print t.timeit(number=10)
