import types
from core.ibs_exceptions import *
from core.db.db_result_wrapper import *
from core import defs

class ibs_db: #abstract parent class for all db implementions. Children must implement esp. query and connect 
    def __init__(self,dbname,host,port,user,password):
        self.connHandle=None
        self.connect(dbname,host,port,user,password)
        self.__addPreparedQueries()

    def __addPreparedQueries(self):
        for table_name in ["users","user_attrs","normal_users","voip_users","persistent_lan_users","caller_id_users"]:
            self.__loadUserPrepareQuery(table_name)
        
        self.prepareQuery("load_normal_users_username",["text"],"select * from normal_users where normal_username = $1")
        self.prepareQuery("load_voip_users_username",["text"],"select * from voip_users where voip_username = $1")
        self.prepareQuery("load_caller_id_users_caller_id",["text"],"select * from caller_id_users where caller_id = $1")
        
    def __loadUserPrepareQuery(self,table_name):
        self.prepareQuery("load_%s"%table_name,["bigint"],"select * from %s where user_id=int8($1)"%table_name)
        self.prepareQuery("bulk_load_%s"%table_name,
                          ["bigint"]*defs.POSTGRES_MAGIC_NUMBER,
                          "select * from %s where %s"%
                           (table_name, \
                            " or ".join(map(lambda i:"user_id=int8($%s)"%i,xrange(1,defs.POSTGRES_MAGIC_NUMBER+1))) \
                           ))

        

    def prepareQuery(self,plan_name, args , query):
        """
            prepare query with name "plan_name" taking arguments "args" and query "query"
            args[list]: list of argument types
        """
        pass

    def executePrepared(self, plan_name, values):
        """
            execute prepared query "plan_name" with list of values "values"
        """
        pass

    def connect(self,dbname,host,port,user,password):
        pass
    
    def _runQuery(self,query):
        """
            run the query, without any exception handleing
            users normally should use query or transactionQuery or IBSQuery class, and should not
            use this method directly
            
        """
        start=time.time()
        try:
            result=self._runQueryDB(query)
            return result
        finally:
            self._logQuery(query, time.time()-start)

    def _runQueryDB(self, query):
        """
            get connection and run the query
        """
        pass

    def query(self,query):
        """
            run the query
        """
        try:
            return self._runQuery(command)
        except Exception,e:
            raise ibs_exceptions.DBException("%s query: %s" %(e,command))


    def transactionQuery(self,query):
        pass

    def runIBSQuery(self,ibs_query):
        """
            run IBS query class queries
        """
        pass

    def _logQuery(self, query, query_time):
        if defs.LOG_DATABASE_QUERIES:
            toLog("Time:%s Query:%s"%(query_time, query),LOG_QUERY)
        
    def getConnection(self):
        if self.connHandle==None:
            raise dbException("None connection")
        return self.connHandle

    def reset(self):
        self.getConnection().reset()
        self.__addPreparedQueries()
    
    def close(self):
        self.getConnection().close()
        self.pgConn=None
    
    def get(self,table,condition="true",from_=0,to=-1,orderBy="",rows=[]):
        """
            orderBy (str or tuple): if it's an string, it will be placed after the order by clause
                                    if it's a tuple, it'll interpreted as (col_name,desc_flag) where desc_flag
                                        is a boolean telling if it should be ordered desc.
        
        """
        query="select "
        if len(rows)==0:
            query+="*"
        else:         
            query+=",".join(rows)

        query += " from " + table 
        if condition:
            query+= " where " + condition + " "
        
        if orderBy:
            order_by_clause=self.__createOrderBy(orderBy)

            query += " order by %s"%order_by_clause

        if from_ >0:
            query +=" offset " + str(from_)
        if to > from_:
            query +=" limit " + str(to-from_)

        return self.selectQuery(query)

    def __createOrderBy(self,order_by):
        if type(order_by)==types.StringType:
            return order_by
        elif type(order_by)==types.TupleType:
            if order_by[1]:     
                desc="desc"
            else:
                desc="asc"
            return "%s %s"%(order_by[0],desc)

    def selectQuery(self,query, result_type=0):
        """
            result_type(int): 0: dictionary
                              1: tuple
                              2: dictionary with wrapper
        """
        result=self.query(query)
        if result_type == 0:
            return self.getDictResult(result)
        elif result_type ==1:
            return self.getTupleResult(result)
        else:
            return self.getDictWrapperResult(result)
    
    def getDictResult(self, result):
        return result.dictresult()
    
    def getTupleResult(self, result):
        return result.getresult()

    def getDicWrapperResult(self, result):
        return DBResultWapper(result)

    def insert(self,table,dict_values):    
        query=createInsertQuery(table,dict_values)
        self.transactionQuery(query)
        
    def update(self,table,dict_values,condition):
        query=createUpdateQuery(table,dict_values,condition)
        self.transactionQuery(query)

    def delete(self,table,condition):
        query=createDeleteQuery(table,condition)
        self.query(query)

    def release(self):
        from core.db import dbpool
        dbpool.release(self)

    def check(self):
        pass

    def seqNextVal(self,seq_name):
        """
            return next value of sequenece "seq_name",
            this supposed to be thread safe
        """
        return self.selectQuery("select nextval('%s')"%seq_name)[0]["nextval"]

    def getCount(self,table,condition):
        """
            return result row count for query with condition "condition" from "table"
        """
        return self.get(table,condition,0,-1,"",["count(*) as count"])[0]["count"]


    

def createInsertQuery(table,dict_values):
    """
        create and return an insert query to insert "dict_values" into "table"
        "dict_values" is in form {column_name=>value}
    """
    if len(dict_values)==0:
        raise DBException("Empty values for insert")
    
    names="("+",".join(dict_values.keys())+")"
    values="("+",".join(map(str,dict_values.values()))+")"
    return "insert into %s %s VALUES %s ;"%(table,names,values)


def createUpdateQuery(table,dict_values,condition):
    """
        create query to update "dict_values" with condition "condition" on "table" 
        dict_value is in form {column_name=>value}
    """
    if len(dict_values)==0:
        raise DBException("Empty values for update")
    set_list=map(lambda name:"%s = %s"%(name,dict_values[name]),dict_values)
    query="update %s set %s where %s ;" % (table,",".join(set_list),condition)
    return query 

def createDeleteQuery(table,condition):
    return "delete from " + table + " where " + condition + ";"

def createFunctionCallQuery(function_name, args):
    """
        create query to call function "function_name" with arguments as "args"
    """
    return "select %s(%s);"%(function_name,",".join(map(str,args)))
