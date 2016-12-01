from core.db import ibs_db
from core.lib.general import *

class UserAuditLog:
    AUDIT_LOG_NOVALUE="_NOVALUE_"

    def userAuditLogQuery(self, admin_id, is_user, obj_id, attr_name, old_value, new_value):
        """
            return query, for inserting a new audit log entry
            admin_id(integer): id of admin performing the job
            is_user(boolean): is destination object a user? if not, it's a group
            obj_id(integer): id of user or group
            attr_name(str): name of attribute that has been changed
            old_value(str): value of attribute before change
            new_value(str): value of attribute after change
        """
        if old_value == new_value :
            return ""
            
        return ibs_db.createFunctionCallQuery("insert_user_audit_log",(admin_id,
                                                                  ("'f'","'t'")[is_user==True],
                                                                  obj_id,
                                                                  dbText(attr_name),
                                                                  dbText(old_value),
                                                                  dbText(new_value)))

    def deleteAuditLogsForUsersQuery(self,user_ids):
        """
            return query for deleting audit logs of users with ids in user_ids
            user_ids(iterable object of user_ids)
        """
        condition=" or ".join(map(lambda user_id:"object_id=%s"%user_id,user_ids))
        return ibs_db.createDeleteQuery("user_audit_log","is_user = 't' and (%s)"%condition)
