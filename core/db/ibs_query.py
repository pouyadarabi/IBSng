from core.ibs_exceptions import *
from core.db import db_main
import types

class IBSQuery:
    """
        IBSQuery is used for large transactions that are more than 8kb. The Query is passed to 
        database backend as many little queries.
    """
    def __init__(self):
        self.__queries=[]

    def __iter__(self):
        return iter(self.__queries)
        
    def __getitem__(self,_index):
        return self.__queries[_index]
    
    def __add__(self,query):
        if query == self: #are we adding ourselves to ourselves?
            raise GeneralException("Can't add an instance of IBSQuery to itself")
            
        if type(query)==types.ListType or isinstance(query,IBSQuery):
            map(self.addQuery,query)
        else:
            self.addQuery(query)
        return self
        
    def addQuery(self,query):
        """
            add a new query to the transaction
        """
        if query:
            self.__queries.append(query)

    
    def runQuery(self):
        """
            run the transaction query
        """
        return db_main.getHandle().runIBSQuery(self)

    def getQueries(self):
        """
            return list of queries
        """
        return self.__queries

    def printQueries(self):
        print "IBSQuery queries:%s"%str(self.__queries)
        