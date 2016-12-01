from core.ibs_exceptions import *

class SearchHelper:
    def __init__(self,conds,requester_obj,requester_role,tables):
        """
            conds(dic like object): dictionary of conditions
            requester_obj(Admin or LoadedUser instance): Admin or user that requested the search
            requester_role(str): "admin" or "user"
            tables(dic): dictionary of database tables involving search in format "table_name":search_table_instance
        """
        self.conds=conds
        self.requester_obj=requester_obj
        self.requester_role=requester_role
        self.tables=tables

    def getRequesterObj(self):
        return self.requester_obj

    def getRequesterRole(self):
        return self.requester_role

    def isRequesterAdmin(self):
        """
            return true if requester is an admin
        """
        return self.requester_role=="admin"

    def getConds(self):
        return self.conds
    
    def hasCondFor(self,*keys):
        for key in keys:
            if not self.conds.has_key(key):
                return False
        return True

    def getCondValue(self,key):
        return self.conds[key]

    def setCondValue(self,key,value):
        self.conds[key]=value

    def getTable(self,table):
        return self.tables[table]

    def createGetIDQuery(self,if_empty_query):
        """
            create a select query, by intersecting all table queries.
            If none of tables has a query, it will return "if_empty_query"
        """
        queries=self.getTableQueries()
        queries=apply(self.filterNoneQueries,queries.values())
        if len(queries)==0:
            query=if_empty_query
        else:
            query=self.intersectQueries(queries)
        return query
        

    def getTableQueries(self):
        table_query={}
        for table_name in self.tables:
            table_query[table_name]=self.tables[table_name].createQuery()
        return table_query

    def filterNoneQueries(self,*args):
        return filter(lambda x:x!=None,args)

    def intersectQueries(self,queries):
        return " intersect ".join(queries)

    def createTempTableAsQuery(self,db_handle,table_name,query):
        db_handle.query("create temp table %s as (%s)"%(table_name,query))

    def dropTempTable(self,db_handle,table_name):
        try:
            db_handle.query("drop table %s"%table_name)
        except:
            logException(LOG_ERROR)

        
