from core.lib.general import *
from core.db.ibs_query import IBSQuery
from core.db import ibs_db,db_main

class ConnectionLogActions:
    TYPES={"internet":1,"voip":2}
    TYPES_REV={1:"internet",2:"voip"}
    
    def logConnectionQuery(self,user_id,credit_used,login_time,logout_time,successful,_type,ras_id,details):
        """
            user_id(int): id of user, this connection is related to
            credit_used(float): amount of credit used by user
            login_time(str): string representaion of user login time
            logout_time(str): string representaion of user logout time
            successful(boolean): was user connection successful, or it failed and user connection didn't established normally in authentication or authorization phase
            _type(str): type of connection, can be "internet" or "voip"
            ras_id(integer): id of ras, connection made to
            details(dictionary): dic of connection details, varying for diffrent types/rases/connections
        """
        names_arr, values_arr = self.__createConnectionDetailsArrays(details)

        return ibs_db.createFunctionCallQuery("insert_connection_log", \
                                                ("%s::bigint"%user_id, 
                                                 credit_used, 
                                                 dbText(login_time), 
                                                 dbText(logout_time), 
                                                 ["'f'","'t'"][successful], 
                                                 "%s::smallint"%self.getTypeValue(_type), 
                                                 ras_id, 
                                                 names_arr, 
                                                 values_arr)
                                              )
    
    def __createConnectionDetailsArrays(self,details):
        names = details.keys()
        values = map(details.get,names) # we want them is same order
        
        names_arr="ARRAY[%s]"%",".join(map(dbText,names))
        values_arr="ARRAY[%s]"%",".join(map(dbText,values))
    
        return names_arr, values_arr

    def getTypeValue(self,_type):
        return self.TYPES[_type]

    def getIDType(self,_id):
        return self.TYPES_REV[_id]
        
        
    def deleteConnectionLogsForUsersQuery(self,user_ids):
        condition=" or ".join(map(lambda user_id:"user_id=%s"%user_id,user_ids))
        details_query=ibs_db.createDeleteQuery("connection_log_details","connection_log_id in (select connection_log_id from connection_log where %s)"%condition)
        connection_query=ibs_db.createDeleteQuery("connection_log",condition)
        return details_query+connection_query
