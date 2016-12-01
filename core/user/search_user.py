"""
select user_id from users where group_id=4 or group_id=5 
intersect 
select user_id from normal_users where username like 'a%' 
intersect 

    (select user_id,count(user_id) from users_attrs where (attr_name='charge_id' and (attr_value='2' or attr_value='3')) or (attr_name='rel_exp_date' and attr_value='2') group by user_id
    union 
    select users_attrs.user_id,count(users_attrs.user_id) from users,users_attrs,group_attrs,groups where users.group_id=groups.group_id and not exists
    (select attr_name from users_attrs where users_attrs.user_id=users.user_id and users_attrs.attr_name='charge_id' or attr_name='rel_exp_date') 
    and group_attrs.attr_name='charge_id' and group_attrs.attr_value='2' );
"""
from core.lib.general import *
from core.db import db_main
from core.report.search_helper import SearchHelper
from core.report.search_table import SearchTable,SearchAttrsTable
from core.report.search_group import SearchGroup

class UserSearchTable(SearchTable):
    def __init__(self,table_name):
        SearchTable.__init__(self,table_name)

    def createQuery(self):
        if not self.getRootGroup().isEmpty():
            table_name=self.getTableName()
            query="select %s.user_id from %s where %s"% \
                (table_name,table_name,self.getRootGroup().getConditionalClause())
            return query

class SearchUsersTable(UserSearchTable):
    def __init__(self):
        UserSearchTable.__init__(self,"users")

class SearchNormalUsersTable(UserSearchTable):
    def __init__(self):
        UserSearchTable.__init__(self,"normal_users")

class SearchPLanUsersTable(UserSearchTable):
    def __init__(self):
        UserSearchTable.__init__(self,"persistent_lan_users")

class SearchCallerIDUsersTable(UserSearchTable):
    def __init__(self):
        UserSearchTable.__init__(self,"caller_id_users")

class SearchVoIPUsersTable(UserSearchTable):
    def __init__(self):
        UserSearchTable.__init__(self,"voip_users")

class SearchUserAttrsTable(SearchAttrsTable):
    def __init__(self):
        SearchAttrsTable.__init__(self,"user_attrs")

    def createQuery(self):
        if not self.getRootGroup().isEmpty():
            return "select user_attrs.user_id from user_attrs where %s"%\
                    (self.getRootGroup().getConditionalClause())

class SearchGroupAttrsTable(SearchAttrsTable):
    def __init__(self):
        SearchAttrsTable.__init__(self,"group_attrs")

    def createQuery(self):
        attrs=self.getAttrs()
        if len(attrs):
            queries=[]
            for attr_name in attrs:
                queries.append("select users.user_id from users,groups,group_attrs \
                    where users.group_id = groups.group_id and \
                    groups.group_id = group_attrs.group_id and \
                    user_id not in (select user_id from user_attrs where attr_name=%s) \
                    and %s"%(dbText(attr_name),attrs[attr_name].getConditionalClause()))
        
            return " union all ".join(queries)

#       if not self.getRootGroup().isEmpty():
#           attr_not_in_user=self.__createNotInUserAttrsClause()
#           return "select users.user_id from users,groups,group_attrs \
#                   where users.group_id = groups.group_id and \
#                   groups.group_id = group_attrs.group_id and \
#                   not exists (select attr_name from user_attrs where user_attrs.user_id = users.user_id and %s) \
#                   and %s"% \
#                   (attr_not_in_user,self.getRootGroup().getConditionalClause())

#    def __createNotInUserAttrsClause(self):
#       group=SearchGroup("or")
#       map(lambda attr_name:group.addGroup("attr_name = %s"%dbText(attr_name)),self.getAttrs())
#       return group.getConditionalClause()
    

class SearchUserHelper(SearchHelper):
    def __init__(self,conds,requester_obj,requester_role):
        SearchHelper.__init__(self,conds,requester_obj,requester_role,
                    {"users":SearchUsersTable(),
                     "user_attrs":SearchUserAttrsTable(),
                     "normal_users":SearchNormalUsersTable(),
                     "persistent_lan_users":SearchPLanUsersTable(),
                     "voip_users":SearchVoIPUsersTable(),
                     "caller_id_users":SearchCallerIDUsersTable(),
                     "group_attrs":SearchGroupAttrsTable(),
                    })

    ############################################
    def getSearchQuery(self):
        """
            return the search query for conditions set in tables. this method take care of empty queries
        """
        query=self.createQuery()
        if query=="":
            query="select user_id from users"
        return query


    def createQuery(self):
        """
            create a database select query, by asking each table to give it's own query.
            WARNING: may return an empty string in case of no conditions
        """
        table_query=self.getTableQueries()
        attrs_query=self.__createAttrsQuery(table_query["user_attrs"],table_query["group_attrs"])
        queries=self.filterNoneQueries(attrs_query,table_query["users"],table_query["normal_users"],table_query["voip_users"],table_query["persistent_lan_users"],table_query["caller_id_users"])
        return self.intersectQueries(queries)

    def __createAttrsQuery(self,user_attrs,group_attrs):
        if user_attrs!= None and group_attrs!=None:
            sub_query="select count(user_id) as count,user_id from (%s union all %s) as all_attrs group by user_id"%(user_attrs,group_attrs)
        elif user_attrs!=None:
            sub_query="select count(user_id) as count,user_id from (%s) as all_attrs group by user_id"%(user_attrs)
        elif group_attrs!=None:
            sub_query="select count(user_id) as count,user_id from (%s) as all_attrs group by user_id"%(group_attrs)
        else:
            return None

        return "select user_id from (%s) as filtered_attrs where count=%s"%(sub_query,len(self.getTable("user_attrs").getAttrs()))
    

    ########################################
    def getUserIDs(self,_from,to,order_by,desc):
        """
            return a tuple of (result_count,user_id_list) 
        """
        query=self.getSearchQuery()
        db_handle=db_main.getHandle(True)
        try:
            self.__createResultTable(db_handle,query)
            result_count=self.__getResultCount(db_handle)
            db_dic=self.__applyOrderBy(db_handle,_from,to,order_by,desc)
        finally:
            self.__dropResultTable(db_handle)
            db_handle.releaseHandle()

        return (result_count,[m["user_id"] for m in db_dic])

    def __createResultTable(self,db_handle,search_query):
        self.createTempTableAsQuery(db_handle,"search_user_temp",search_query)

    def __dropResultTable(self,db_handle):
        self.dropTempTable(db_handle,"search_user_temp")
        
    def __getResultCount(self,db_handle):
        return db_handle.getCount("search_user_temp","true")

    def __applyOrderBy(self,db_handle,_from,to,order_by,desc):
        order_by_tables={"normal_username":"normal_users",
                         "voip_username":"voip_users",
                        "user_id":"users",
                        "group_id":"users",
                        "creation_date":"users",
                        "owner_id":"users",
                        "credit":"users",
                        "first_login":"user_attrs"
                       }
        if order_by in order_by_tables:
            table=order_by_tables[order_by]
        else:
            table=None #no order by
                
        if table=="users":
            return self.__usersOrderBy(db_handle,_from,to,order_by,desc)
        elif table in ["normal_users","voip_users"]:
            return self.__usernameOrderBy(db_handle,_from,to,order_by,desc,table)
        elif table == "user_attrs":
            return self.__userAttrsOrderBy(db_handle,_from,to,order_by,desc)
        else:
            return self.__emptyOrderBy(db_handle,_from,to)

    def __usersOrderBy(self,db_handle,_from,to,order_by,desc):
        return db_handle.get("users join search_user_temp using (user_id)","",_from,to,(order_by,desc),("users.user_id",))

    def __userAttrsOrderBy(self,db_handle,_from,to,order_by,desc):
        return db_handle.get("search_user_temp left join user_attrs on (search_user_temp.user_id=user_attrs.user_id and user_attrs.attr_name=%s)"%(dbText(order_by)),
                             "",_from,to,("attr_name",desc),("search_user_temp.user_id",))

    def __emptyOrderBy(self,db_handle,_from,to):
        return db_handle.get("search_user_temp","true",_from,to,"")

    def __usernameOrderBy(self,db_handle,_from,to,order_by,desc,table):
#       return self.__handleBySortCol(db_handle,_from,to,order_by,desc,table)
        return db_handle.get("search_user_temp left join %s on (search_user_temp.user_id=%s.user_id)"%(table,table),
                             "",_from,to,(order_by,desc),("search_user_temp.user_id",))

    #####################################
    def __handleBySortCol(self,db_handle,_from,to,order_by,desc,table):
        """
            handle sorting by creating a new column and sorting the select query
            
            CURRENTLY UNUSED
        """
        self.__addSortCol(db_handle,"text")
        self.__updateSortCol(db_handle,order_by,table)
        return self.__sortColOrderBy(db_handle,_from,to,desc)

    def __addSortCol(self,db_handle,_type):
        db_handle.query("alter table search_user_temp add sort_col %s"%_type)

    def __updateSortCol(self,db_handle,order_by,table):
        db_handle.query("update search_user_temp set sort_col=%s from %s where search_user_temp.user_id=%s.user_id"%(order_by,table,table))
        
    def __sortColOrderBy(self,db_handle,_from,to,desc):
        return db_handle.get("search_user_temp","true",_from,to,("sort_col",desc),("user_id",))
    #######################################
